pyenv:
	mkdir -p .env
	virtualenv .env
	. .env/bin/activate; pip install -r requirements.txt

application.pdf:	robert-seward-blue.pdf ~/Sync/mydocs/resume/covers/2024/uniteus-devopsengineer.pdf 
	rm -f application.pdf
	pdfunite ~/Sync/mydocs/resume/covers/2024/clps-pythonsendev.pdf robert-seward-blue.pdf application.pdf
	evince application.pdf

lint:
	ruff check

runui:
	./runui.sh




