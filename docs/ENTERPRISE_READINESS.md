# Cloud Secure Hospital ERP — Enterprise Upgrade Pack

This package upgrades the existing desktop ERP with an **AI Hospital Intelligence Center** and a safer path toward enterprise deployment.

## Included

- AI Intelligence Center in the dashboard
- Read-only, schema-aware operational metrics
- Deterministic operational alerts for appointments, lab queue, stock, expiry and IPD
- Controlled AI prompt that uses aggregate metrics only
- Role permission for AI Intelligence (Super Admin/Admin)
- Offline AI mode when no API key is configured
- `.env.example` configuration template
- Enterprise readiness documentation

## Important production boundary

This is an **enterprise demo / pre-production build**, not a certified clinical system. Before a real hospital deployment, complete legal, security, privacy, clinical-safety and compliance review appropriate to the deployment jurisdiction and hospital.

Do not use the AI layer to diagnose, prescribe, triage, or autonomously make clinical decisions.

## Live AI configuration

Set `OPENAI_API_KEY` and `HOSPITAL_AI_MODEL` in the runtime environment. The model name must be one that is actually enabled for the account. Never commit API keys into source control.

If these variables are absent, the application continues in offline rule-based mode for supported operational questions.

## Recommended enterprise hardening before sale/deployment

1. Move from local SQLite to a managed multi-user database for network deployment.
2. Add centralized authentication/SSO, MFA and stronger password hashing.
3. Encrypt data in transit and at rest; manage keys outside the application source.
4. Add immutable audit logging for security-sensitive actions.
5. Define backup, restore, disaster-recovery and retention procedures.
6. Perform dependency, SAST, DAST and penetration testing.
7. Add formal role/least-privilege review for every module and report.
8. Add monitoring, alerting, error tracking and centralized logs.
9. Validate all patient-facing/clinical workflows with qualified hospital staff.
10. Complete applicable privacy, health-data and regulatory assessment before production use.
