# Phase 6 — Full Production Integration Foundation

## What changed
- Added an approved-module server gateway for Patients, Doctors, Appointments, Laboratory, Pharmacy, Inventory and Billing.
- Added server-side RBAC for read/write operations.
- Added approved-field allowlists to reduce accidental exposure of unrelated database columns.
- Added pagination and server-side search.
- Added centralized enterprise dashboard endpoint.
- Added audit events for module reads/writes/deletes and denied operations.
- Added a desktop `RemoteGateway` client for the centralized API.
- Added a server-backed Enterprise AI Center.

## Deployment model
Hospital workstations run the compiled client. The API server owns the central database and AI provider credentials.

## Production requirements before live patient use
1. Put the API behind a managed TLS reverse proxy.
2. Replace development API/JWT secrets with random secrets from a secret manager.
3. Use a supported production database and automated backups.
4. Add MFA/SSO for privileged accounts.
5. Perform penetration testing and vulnerability scanning.
6. Validate applicable healthcare/privacy obligations with the hospital's compliance/legal team.
7. Configure monitoring, alerting and disaster recovery.
8. Migrate each existing UI CRUD screen to `RemoteGateway` before disabling local writes.

## Important
Phase 6 provides the centralized API integration foundation. Existing legacy local CRUD screens are intentionally not silently switched to remote mode; each module should be migrated and tested separately to avoid data loss.
