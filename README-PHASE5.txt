PHASE 5 - CLIENT/SERVER INTEGRATION

Developer:
1. Configure server/.env.server.example as a server-only environment.
2. Install requirements-server.txt.
3. Run START-API-SERVER-DEV.bat for development.
4. Keep API keys, JWT secret, database and AI provider keys on the server.
5. Use HTTPS/TLS in production.

Hospital:
The hospital should receive only the compiled EXE and deployment configuration. Never distribute the developer source, SQLite database, API provider key, or server .env.

Phase 5 adds server/client.py and frontend/ai/remote_ai_center.py for server-backed AI. Full migration of every ERP CRUD operation to the API is a subsequent production migration step.
