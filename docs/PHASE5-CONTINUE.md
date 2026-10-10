# Phase 5 — ERP Client/Server Integration

This release adds a server-backed AI center and hardened API client.

## Architecture
Hospital EXE -> HTTPS -> FastAPI -> controlled service methods -> database/AI.

## Important
The existing local ERP modules remain available for development. Production should progressively move sensitive operations behind authenticated service endpoints. Do not expose SQLite, arbitrary SQL, API secrets, or model keys to the hospital client.

## Production requirements
- HTTPS/TLS with a valid certificate
- MFA/SSO where required
- Centralized audit logging
- Encrypted backups and tested recovery
- Server firewall/network segmentation
- Secret manager instead of .env for production
- Penetration testing and vulnerability management
- Applicable healthcare/privacy compliance review
