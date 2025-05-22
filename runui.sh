#!/bin/bash

# Activate the python virtual env
. .env/bin/activate

if [ -z "$GOOGLE_API_KEY" ] ; then
    echo "This application requires a GOOGLE_API_KEY to connect to the Google Gemini API."
    echo "Please set or obtain a key to use this tool!"
    exit 1
fi

# Run the app
streamlit run analyzedocs_resume_slui.py
