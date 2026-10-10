# Phase 4 Continued - Enterprise Client/Server

## Architecture
Hospital desktop client -> HTTPS -> API gateway -> centralized DB/AI.

## Added
- API-key gate for trusted desktop clients
- Username/password login against the server user table
- Short-lived JWT sessions
- Role-based protected endpoints
- Login rate limiting in the API process
- Summary endpoint with operational metrics
- Admin security endpoint
- Safe-mode AI endpoint
- Desktop `server/client.py` API client

## Production requirements
1. Put the API behind HTTPS (reverse proxy/load balancer).
2. Set `ERP_API_KEY` and a cryptographically random `ERP_JWT_SECRET` on the server.
3. Move the database to a protected server volume; do not ship it inside the client.
4. Replace the sample API URL in the desktop client's secure configuration.
5. Use MFA/SSO, centralized audit logs, backups, monitoring and penetration testing before production.
6. Do not treat this package as healthcare compliance certification.
