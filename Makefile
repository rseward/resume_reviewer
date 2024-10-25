pyenv:
	mkdir -p .env
	virtualenv .env
	pip install -r requirements.txt

application.pdf:	robert-seward-blue.pdf ~/Sync/mydocs/resume/covers/2024/oracle-softengineersec.pdf
	rm -f application.pdf
	#pdf-stapler cat ~/Sync/mydocs/resume/covers/2024/davant-cloudengineer.pdf robert-seward-blue.pdf application.pdf
	#pdf-stapler cat ~/Sync/mydocs/resume/covers/2024/uofm-sitereliability.pdf robert-seward-blue.pdf application.pdf
	pdf-stapler cat ~/Sync/mydocs/resume/covers/2024/oracle-softengineersec.pdf robert-seward-blue.pdf application.pdf
	#pdf-stapler cat ~/Sync/mydocs/resume/covers/2024/duo-softwarearch.pdf robert-seward-blue.pdf application.pdf
	evince application.pdf

runui:
	streamlit run analyzedocs_resume_slui.py




