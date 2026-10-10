# Hospital Installation Guide

## Server
1. Provision an approved Linux/Windows server or cloud environment.
2. Configure PostgreSQL and Redis where required.
3. Configure environment secrets outside source control.
4. Configure TLS certificates.
5. Start API and reverse proxy services.
6. Verify `/health` and production smoke tests.
7. Configure backups and perform a restore drill.

## Client
1. Install the signed ERP installer on an approved workstation.
2. Configure the approved API endpoint.
3. Create/assign the user's account.
4. Verify role permissions.
5. Complete a UAT smoke test.

Do not copy developer source code, `.env` files containing secrets, or production database files to client PCs.
