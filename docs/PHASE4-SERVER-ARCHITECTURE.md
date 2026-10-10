# Phase 4 — Server-Based Enterprise Architecture

## Target architecture

Hospital Windows clients -> HTTPS/TLS -> ERP API server -> database + AI service

### Why this is better
- Source code and AI provider secrets are not distributed to hospital PCs.
- Centralized authentication, authorization, audit, backups and updates are possible.
- Multiple reception/doctor/lab/pharmacy clients can use one controlled backend.

## Production hardening checklist

- [ ] Deploy API only behind HTTPS/TLS.
- [ ] Use a real identity provider or strong server-side authentication with MFA.
- [ ] Replace API-key-only authentication with short-lived user tokens and RBAC.
- [ ] Put the database on a protected server/network, not a public endpoint.
- [ ] Encrypt backups and test restoration.
- [ ] Centralize audit logs and restrict access.
- [ ] Store AI/API secrets only on the server.
- [ ] Add rate limits, request validation, CSRF protections where applicable, and security headers.
- [ ] Perform dependency scanning, SAST and penetration testing before clinical deployment.
- [ ] Complete the hospital's applicable privacy/security/compliance review before using real patient data.
