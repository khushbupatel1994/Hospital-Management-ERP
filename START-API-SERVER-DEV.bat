@echo off
call .venv\Scripts\activate
set ERP_API_KEY=DEV-CHANGE-ME
set ERP_JWT_SECRET=DEV-ONLY-CHANGE-ME-32-CHAR-SECRET
set HOSPITAL_DB=C:\Users\hp\AppData\Local\Cloud Secure Hospital ERP\database\hospital.db
python -m uvicorn server.app:app --host 127.0.0.1 --port 8000 --reload
