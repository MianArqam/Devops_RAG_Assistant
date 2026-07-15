Set-Location "$PSScriptRoot\..\backend"
if (-not (Test-Path ".venv")) {
  python -m venv .venv
}
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt
if (-not (Test-Path ".env")) {
  Copy-Item ".env.example" ".env"
}
.\.venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
