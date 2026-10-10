# Phase 10 — Production Deployment & Hospital Pilot

This package adds production deployment scaffolding and verification helpers. It does **not** claim that external penetration testing, legal/privacy approval, TLS certificate issuance, or code signing has occurred.

## Production topology

Hospital client -> HTTPS/Nginx -> API -> PostgreSQL + Redis -> backup/monitoring.

## Before go-live

1. Provision PostgreSQL and Redis on secured infrastructure.
2. Set secrets only in the server environment/secret manager.
3. Configure a CA-issued TLS certificate; do not use demo certificates for production.
4. Map and test the existing schema before migrating data.
5. Run backup + restore drills and document RPO/RTO.
6. Run UAT with hospital representatives.
7. Complete an independent penetration test and remediate findings.
8. Complete privacy/security/legal review applicable to the deployment.
9. Build and code-sign the Windows client on a controlled Windows build machine.
10. Pilot before production go-live.
