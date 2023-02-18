compile:
	rm -rf dist/
	pyinstaller --onefile -y --name main main.py
	rm main.spec