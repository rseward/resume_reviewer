pyenv:
	mkdir -p .env
	virtualenv .env
	pip install -r requirements.txt

application.pdf:	robert-seward-blue.pdf ~/Sync/mydocs/resume/covers/2024/oracle-softengineersec.pdf
	rm -f application.pdf
	pdfunite ~/Sync/mydocs/resume/covers/2024/oracle-softengineersec.pdf robert-seward-blue.pdf application.pdf
	evince application.pdf

runui:
	streamlit run analyzedocs_resume_slui.py




