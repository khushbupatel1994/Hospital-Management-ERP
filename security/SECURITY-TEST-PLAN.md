# Security Test Plan — Phase 9

This plan prepares the ERP for an independent penetration test. It does not claim that a penetration test has been completed.

## Scope
- Desktop client authentication/session handling
- API authentication and authorization
- RBAC and object-level access control
- Input validation and injection resistance
- File upload/download controls
- Rate limiting and abuse controls
- Audit logging and sensitive-data exposure
- AI gateway prompt/data boundary
- TLS/reverse-proxy configuration
- PostgreSQL/Redis network exposure

## Required workflow
1. Freeze a release candidate.
2. Run automated tests and dependency scanning.
3. Run an independent penetration test in a non-production environment.
4. Record findings with severity, evidence, owner and due date.
5. Fix Critical/High findings before pilot deployment.
6. Retest fixes and obtain written sign-off.

## Evidence to retain
- Test scope and authorization
- Tool/version list
- Findings report
- Remediation commits/build IDs
- Retest report
- Final security sign-off
