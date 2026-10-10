# Final Enterprise Architecture

Hospital workstations run a source-free signed desktop client. The client communicates over HTTPS with the central API. Authentication, RBAC, audit logging, business rules and AI orchestration remain server-side. PostgreSQL is the system of record; Redis can provide centralized session/revocation/cache functions. Nginx terminates TLS and rate-limits traffic. Prometheus provides infrastructure metrics.

## Security boundary
Desktop client: UI only; no production secrets.
API server: identity, authorization, validation, audit and business logic.
Database: private network, least privilege, encrypted backups.
AI provider: server-side key only; send the minimum necessary data.

## AI safety
AI is an administrative/decision-support feature. It must not autonomously diagnose, prescribe, or override clinicians. Patient-facing outputs require appropriate human review.
