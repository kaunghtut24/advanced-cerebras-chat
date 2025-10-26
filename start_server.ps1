# Starting Cerebras Chat Interface with SSL fix
Write-Host "Starting Cerebras Chat Interface with SSL fix..." -ForegroundColor Green

# Set the correct SSL certificate bundle path
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$CertPath = Join-Path $ScriptPath "venv\Lib\site-packages\certifi\cacert.pem"

$env:REQUESTS_CA_BUNDLE = $CertPath
$env:SSL_CERT_FILE = $CertPath

# Disable SSL verification for Hugging Face downloads
$env:HF_HUB_DISABLE_SSL = "1"
$env:PYTHONHTTPSVERIFY = "0"

Write-Host "SSL certificate path set to: $CertPath" -ForegroundColor Yellow

# Activate virtual environment and start the server
try {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & "$ScriptPath\venv\Scripts\Activate.ps1"
    
    Write-Host "Starting server..." -ForegroundColor Cyan
    & python app.py
}
catch {
    Write-Host "Error occurred: $_" -ForegroundColor Red
    pause
}
