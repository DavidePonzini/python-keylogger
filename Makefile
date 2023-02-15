compile:
	rm -rf dist/
	pyinstaller --onefile -y --name keylogger main.py