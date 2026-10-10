# Phase 4 deployment

## Developer/server
- Install Python 3.11+.
- Create a virtual environment and install `requirements-server.txt`.
- Set `ERP_API_KEY`, `ERP_JWT_SECRET`, and `HOSPITAL_DB` as server environment variables.
- Run behind a real HTTPS reverse proxy; do not expose the Uvicorn development listener directly to the public internet.
- Store the database outside the client package and back it up.

## Hospital client
- Ship only the compiled desktop client.
- Configure only the HTTPS API URL and client credential mechanism.
- Never ship `.env.server`, database files, or AI provider keys.

## Verification
- `GET /health` should return status `ok`.
- Login uses the server-side `users` table and returns a short-lived JWT.
- `/api/v1/summary` requires a valid JWT.
- `/api/v1/admin/security` requires Super Admin/Admin role.
- `/api/v1/ai/assistant` requires a valid JWT and remains in safe-mode.

## Production hardening still required
MFA/SSO, centralized audit logging, key rotation, TLS certificate management, firewall rules, rate limiting at the reverse proxy, database encryption/backup, monitoring, disaster recovery, vulnerability scanning, penetration testing, and an applicable legal/privacy/compliance review.
