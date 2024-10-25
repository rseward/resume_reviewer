import google.generativeai as genai

def upload_pdf(fname):
    return upload_to_gemini(fname, mime_type="application/pdf")

def upload_txt(fname):
    return upload_to_gemini(fname, mime_type="text/plain")


def upload_to_gemini(path, mime_type=None):
    """Upload a given file to gemini

    See https://ai.google.dev/gemini-api/docs/prompting_with_media
    """
    ufile = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{ufile.display_name}' as: {ufile.uri}")

    return ufile

def wait_for_file_activation(files):
    """Waits for a set of files to be active in the context.

       Files generally need to be processed after upload. This method checks the status of the files
      by checking their "state" field.

      This implementation blocks and polls for the state to transition. A more sophiscated approach
      is likely more appropriate in other contexts."""

    print("Waiting for files to be processed...")
    for name in (ufile.name for ufile in files):
        ufile = genai.get_file(name)
        while ufile.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            ufile.get_file(name)
        if ufile.state.name != "ACTIVE":
            raise Exception(f"File {ufile.name} failed to process")
    print(f"... {len(files)} ready.\n")
