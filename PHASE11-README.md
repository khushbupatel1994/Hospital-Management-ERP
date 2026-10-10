# Phase 11 — Production Pilot Release Candidate

This package consolidates Phase 1–10 and adds the final engineering release-candidate layer.

## Added
- Preflight validation for required environment variables and production safety flags
- PostgreSQL connectivity/migration preflight without modifying data
- Backup manifest + SHA-256 integrity verification
- Restore-drill wrapper with explicit confirmation guard
- Production deployment smoke-test script
- Windows release checklist and installer handoff
- Hospital pilot acceptance gate and rollback plan
- Central release manifest with SHA-256 hashes
- Final status report that distinguishes automated checks from external gates

## Important
This is a release-candidate engineering package, not a claim of medical/legal certification. Independent penetration testing, hospital UAT sign-off, privacy/legal review, TLS certificate issuance, code-signing certificate issuance, and production infrastructure approval remain external gates.
