# resume_reviewer

Simple AI project for reviewing a resume against a job description.

## Credits

This project was inspired by these youtube videos. Please watch them before you get started running this project.

- https://www.youtube.com/watch?v=lig9c7OkxTI
- https://www.youtube.com/watch?v=ztBJqzBU5kc

## How to use this

The original program from the youtube video was setup to use ollama / llama3.2 local model using RAG. As this was
a fair bit more complicated to setup and use. I opted to refactor the project idea to use Google Gemini model. If there
is interest in the ollama / llama3.2 project I can create a project for that as well.

These instructions assume a Linux like envioronment. It could be run in a pure Windows environment that supports python, but I will
leave that as an exercise for the reader. If you capture such platform specific instructions please share them and I will make sure they
added to this document.

One alternative to using this on Windows would be to run it inside a ubuntu WSL environment.

### Step 0

```
make pyenv
```

This step sets up a python virtual environment with the required modules dependencies. I have been using this project with Python 3.12.
I would suggest doing the same, but feel free to try what you have available to you.

### Step 1

_Obtain a google gemini api key._ I suggest typing this into google `how to setup google gemini api key` and you should be able
to acquire your key in about 5 to 10 minutes.

### Step 2

Save your API key to a safe and secure spot. I save mine to a file called `myenv`

For example myenv file looks something like this:

```
. .env/bin/activate # Activate the project virtual environment
export GOOGLE_API_KEY=BLAHyourreallylong_googleapikey
```

### Step 3

The project focuses on PDF documents as those are easy to distribute to hiring managers and AI RAG processors alike.

The project Makefile will "staple" your resume to your cover letter. The combined document is called application.pdf and
can be uploaded to the streamlit UI that the project presents.

So once you have prepared your resume and cover letter. Export them as PDFS. Edit the Makefile to prepare an appropriate
application.pdf

```
make application.pdf
```

This will "staple" the documents together and it will give you a chance to look the cover letter / resume document over before using the UI.

### Step 4

Start the python project and it's streamlit UI.

```
make runui
```

This should start the web app and a browser window pointed to the interface running on the local machine. Please note the current project runs locally
but uses Google Gemini for generating a response. Ergo your document will be sent to Gemini to produce a response. If this is unacceptable, the original
inspiration for this project is based on ollama and local models. Personally that implementation is a far bit more complicated and the results it
produces is a little less cogent in my opinion.

### Step 5

Use the UI to evaluate your suitability to a job position listing.

I find a suitable position I want to apply to. I copy and paste the Job Posting requirements to a spreadsheet.

I later cut and paste this same set of requirements to this interface.

Return to the browser window with the UI.

#### UI Step 1

Click the Browse files button to upload the application.pdf document you created earlier.

#### UI Step 2

In the job description text area, paste the job posting description.

#### UI Step 3

In the chat area at the bottom of the right side. Find the "Enter a prompt here" chat text field.

Enter text like this:

`Please summarize the strengths and weaknesses of the candidate for this position.`

You can enter any text that you want here. But this is the prompt I am using and produces a reasonable good result for my purposes.

Click the send button. Gemini should spend ten seconds or so evaluating the request. It should finish and provide a critique of your
candidacy for the position.

You can ask it more questions about your document. The AI is quite general and not specific for this task what's so ever. It will read
and respond as appropriate to the combination of the PDF document given, the job description text area and the chat message history.

You could use this interface to interograte the latet version of D&D rules if you have a PDF of the rules. And then start asking questions
about the game rules in the text.

#### UI Step 4

If you would like to repeat the process for another iteration or position. Click on the "Delete Session"

Delete the application.pdf document you attached as well.

Return to `UI Step 1` and you should be able to do it all again if you like.

## A sample prompt

I personally have found this prompt useful for using this model / app:

```
Please summarize the strengths and weaknesses of the candidate for this position.
```

You can cut and paste that sentence into the chat prompt entry in the UI or write your question.



