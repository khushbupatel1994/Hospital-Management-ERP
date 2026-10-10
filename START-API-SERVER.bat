@echo off
setlocal
if not exist .venv python -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements-server.txt
if "%ERP_API_KEY%"=="" echo WARNING: Set ERP_API_KEY before production.
if "%ERP_JWT_SECRET%"=="" echo WARNING: Set ERP_JWT_SECRET before production.
python -m uvicorn server.app:app --host 0.0.0.0 --port 8443
