#!/usr/bin/env python

"""
ollama document chat with a streamlit front end modified to talk with google gemini

- https://www.youtube.com/watch?v=lig9c7OkxTI
- https://www.youtube.com/watch?v=ztBJqzBU5kc

"""

import os
import time
import google.generativeai as genai
import streamlit as st
import logging
import tempfile
import shutil
import pdfplumber
import icecream as ic

GEMINI_MODELS=[ "gemini-1.5-pro", "gemini-1.5-flash" ]
from typing import List, Tuple, Dict, Any, Optional

# Streamlit page configuration
st.set_page_config(
    page_title='Google Gemini PDF RAG Streamlit UI',
    page_icon='📚',
    layout='wide',
    initial_sidebar_state='collapsed'
)

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def is_empty( sval: str) -> bool:
    if sval is not None:
        if len(sval.strip())>0:
            return False
    return True

def create_gemini_model(selected_model: str):
    # Create our model
    model_gen_config = {
        "temperature": 1, # lower this value if we only want retrieval from the source data and no added inferences.
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain"
        }

    logger.info( f"Creating Model: {selected_model}")
    model = genai.GenerativeModel(
        model_name=selected_model,
        generation_config=model_gen_config,
        # adjust safety settings as necessary
        )

    return model
    
from gemini_rag import upload_pdf, wait_for_file_activation

def upload_file_action(file_upload):
    temp_dir = tempfile.mkdtemp()
    
    gfileref = None
    tfile = os.path.join(temp_dir, file_upload.name)
    with open(tfile, "wb") as f:
        f.write(file_upload.getvalue())
        logger.info(f"File saved to temporary path: {tfile}")

        gfileref = upload_pdf(tfile)

    return [ gfileref ]

def create_model_session(selected_model: str, gfilerefs: list, jobdesc: str) -> tuple:
    model = create_gemini_model(selected_model)
    wait_for_file_activation(gfilerefs)

    assert not(is_empty(jobdesc)), "Please enter a job description." 

    history=[]
    for gfileref in gfilerefs:
        history.append(
            {
                "role": "user",
                "parts": [
                    gfileref,
                    "Please analyze the document above for reference in the questions to follow.\n\n",
                ]
            }
        )

    print( jobdesc )
    history.append(
        {
            "role": "user",
            "parts": [
                f"""JOB DESCRIPTION:
                {jobdesc}
                """,
                "Please assess the strengths and weaknesses for suitability to the job description provided above."
            ]
        }
    )
    
    chat_session = model.start_chat( history=history )
    print( "model_type: %s cs_type %s" % (str(type(model)), str(type(chat_session) ) ) ) 

    
    return (model, chat_session)


    
def process_question(model, chat_session, question: str, gfilerefs: List) -> str:
    """
    Process a user question using the vector database and selected language model
    
    Args:
        question (str): The user's question.
        vector_db (Milvus): The vector database containing document embeddings.
        selected_model (str): The name of the selected language model.

    Returns:
        str: The generated response to the user's question.
    """
    logger.info(f"Processing question: {question}")
    response = chat_session.send_message( question )

    logger.info("Question processed and response generated")
    try:
        return response.text
    except:
        return response

@st.cache_data
def extract_all_pages_as_images(file_upload) -> List[Any]:
    """
    Extract all pages from a PDF file as images.
    Args:
        file_upload (st.UploadedFile): Streamlit file upload object containing the PDF.
    Returns:
        List[Any]: A list of image objects representing each page of the PDF.
    """
    logger.info(f"Extracting all pages as images from file: {file_upload.name}")
    pdf_pages = []
    with pdfplumber.open(file_upload) as pdf:
        pdf_pages = [page.to_image().original for page in pdf.pages]
    logger.info("PDF pages extracted as images")
    return pdf_pages

def delete_session(pdf_pages) -> None:
    """
    Delete the vector database and clear related session state.

    Args:
        pdf_pages: Set of pdf_pages from the document
    """
    logger.info("Deleting Session")
    if pdf_pages is not None:
        st.session_state.pop("pdf_pages", None)
        st.session_state.pop("file_upload", None)
        st.session_state.pop("gfiles", None)        
        st.session_state.pop("model", None)
        st.session_state.pop("messages", None)        
        st.session_state.pop("chat_session", None)
        st.success("Session state deleted successfully.")
        logger.info("Session state deleted successfully.")
        st.rerun()
    else:
        st.error("No session to delete.")
        logger.warning("No session to delete.")

def main() -> None:
    """
    Main function to run the Streamlit application.

    This function sets up the user interface, handles file uploads,
    processes user queries, and displays results.
    """
    selected_model = None
    st.subheader("🧠 Google Gemini PDF RAG playground", divider="gray", anchor=False)

    col1, col2 = st.columns([1.5, 2])

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    if "pdf_pages" not in st.session_state:
        st.session_state[ "pdf_pages" ] = None
    a = st.session_state[ "pdf_pages" ]
    pdf_pages = a if a is not None else [] 

    if "gfiles" not in st.session_state:
        st.session_state[ "gfiles" ] = None
    
    available_models=GEMINI_MODELS
    if available_models:
      selected_model = col2.selectbox(
        "Pick a Gemini model", available_models
      )

    file_upload = col1.file_uploader(
        "Upload a PDF file ", type="pdf", accept_multiple_files=False
    )

    if file_upload and st.session_state[ "gfiles"] is None:
        st.session_state["file_upload"] = file_upload
        st.session_state[ "gfiles" ] = upload_file_action( file_upload )
        pdf_pages = extract_all_pages_as_images(file_upload)
        st.session_state["pdf_pages"] = pdf_pages

    if file_upload and selected_model:
        if st.session_state.get("model") is None and not(is_empty(st.session_state["jobdesc"])):
            (model, chat_session ) = create_model_session( selected_model, st.session_state[ "gfiles" ], st.session_state["jobdesc"] )
            st.session_state[ "model" ] = model
            st.session_state[ "chat_session" ] = chat_session

    zoom_level = col1.slider(
        "Zoom Level", min_value=100, max_value=1000, value=700, step=50
    )

    with col1:
        with st.container(height=510, border=True):
            for page_image in pdf_pages:
                st.image(page_image, width=zoom_level)
        st.session_state[ "jobdesc" ] = st.text_area( label="Job Description", value="", height=400, placeholder="Enter job description" )
                
    delete_session_btn = col1.button("🗑️ Delete session", type="secondary")

    if delete_session_btn:
        delete_session(st.session_state["pdf_pages"])

    with col2:
        message_container = st.container(height=800, border=True)

        for message in st.session_state["messages"]:
            avatar = "🤖" if message["role"] == "assistant" else "😎"
            with message_container.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        if prompt := st.chat_input("Enter a prompt here..."):
            try:
                st.session_state["messages"].append({"role": "user", "content": prompt})
                message_container.chat_message(
                  "user", avatar="😎").markdown(prompt)

                with message_container.chat_message("assistant", avatar="🤖"):
                    with st.spinner(":green[processing...]"):
                        if st.session_state["chat_session"] is not None:
                            response = process_question(
                                st.session_state[ "model" ],
                                st.session_state[ "chat_session" ],
                                prompt,
                                st.session_state["gfiles"]
                            )
                            st.markdown(response)
                        else:
                            st.warning("Please upload a PDF file first.")
                            
                if st.session_state["chat_session"] is not None:
                    st.session_state["messages"].append(
                        {"role": "assistant", "content": response}
                    )
            except Exception as e:
                st.error(e, icon="🚨")
                logger.error(f"Error processing prompt: {e}")
        else:
            if st.session_state["pdf_pages"] is None:
                st.warning("Upload a PDF file and enter a Job Description to begin chat...")

if __name__ == "__main__":
    main()
    
# Please summarize the strengths and weaknesses of the candidate for this position.
# Analyze the sentiment of the cover letter portion of the candidates submission.


