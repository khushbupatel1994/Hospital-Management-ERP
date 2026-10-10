# Final Release Status — Phase 11

## Engineering status
The software package includes the Phase 1–10 architecture plus Phase 11 release-candidate tooling. Automated checks can validate code, configuration shape, hashes, backups, and deployment smoke tests when run against the real environment.

## Not automatically completed
The following require real organizational/external execution:
- Penetration testing and retest
- Hospital UAT/sign-off
- Privacy/legal/compliance approval
- Production TLS certificate
- Code-signing certificate and signed Windows installer
- Production PostgreSQL/Redis infrastructure
- Disaster-recovery restore drill on the hospital environment

## Release rule
The application must not be represented as production-certified until every required external gate is signed off.
