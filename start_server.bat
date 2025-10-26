@echo off
echo Starting Cerebras Chat Interface with SSL fix...

REM Set the correct SSL certificate bundle path
set REQUESTS_CA_BUNDLE=%~dp0venv\Lib\site-packages\certifi\cacert.pem
set SSL_CERT_FILE=%~dp0venv\Lib\site-packages\certifi\cacert.pem

REM Disable SSL verification for Hugging Face downloads
set HF_HUB_DISABLE_SSL=1
set PYTHONHTTPSVERIFY=0

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the server
python app.py

pause
