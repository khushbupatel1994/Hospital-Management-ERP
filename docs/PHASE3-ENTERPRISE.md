# Phase 3 — Enterprise Hospital ERP

## Included
1. Windows executable packaging path using PyInstaller.
2. Hospital distribution excludes Python source code.
3. Enterprise audit log with HMAC hash chaining.
4. Idle-session guard utility.
5. Database integrity and core-table health checks.
6. Local deployment license gate utility.
7. Dedicated developer build and hospital build scripts.
8. AI remains a controlled operational assistant, not an autonomous clinical decision-maker.

## Important IP note
A packaged executable hides ordinary `.py` files from hospital staff, but no client-side executable can guarantee that code is impossible to reverse engineer. Keep proprietary algorithms and AI orchestration on a server for stronger IP protection.

## Recommended production architecture
Hospital PCs -> HTTPS/API Gateway -> Application Server -> Database Server
                                  |-> AI Service
                                  |-> Audit Log Store
                                  |-> Backup Store

Do not put the production database or AI API secret inside a public/shared installer.

## Pre-production gates
- penetration test
- backup restore test
- role/permission review
- MFA for privileged users
- TLS for network traffic
- centralized audit retention
- OS patching and endpoint protection
- privacy/security legal review for the target country and hospital
- clinical governance review for any clinical decision-support feature
