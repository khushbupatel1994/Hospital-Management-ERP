# Production Go-Live Checklist

This package is an enterprise deployment foundation, not a healthcare certification.

## Before go-live
- [ ] Obtain hospital security/privacy approval and document applicable Indian and contractual requirements.
- [ ] Run a third-party penetration test and remediate findings.
- [ ] Provision PostgreSQL on a private network; disable public database access.
- [ ] Enable TLS 1.2/1.3 with a valid certificate and rotate certificates on a schedule.
- [ ] Configure MFA for privileged users; prefer SSO/IdP integration for larger hospitals.
- [ ] Move API/AI/database secrets into a secrets manager; never ship them in the desktop client.
- [ ] Migrate and validate production data in staging before cutover.
- [ ] Configure encrypted backups and perform a full restore drill.
- [ ] Configure centralized logs/alerts and restrict monitoring endpoints.
- [ ] Configure least-privilege service accounts and OS firewall rules.
- [ ] Sign the Windows installer/application with the organization's code-signing certificate.
- [ ] Establish incident response, access review, retention and disaster-recovery procedures.

## Cutover
1. Freeze writes to the old system.
2. Take a verified backup.
3. Migrate to PostgreSQL.
4. Reconcile record counts and critical financial/clinical totals.
5. Enable API + TLS + monitoring.
6. Pilot with a small staff group.
7. Roll out department by department.
8. Keep rollback backup until the agreed retention period expires.
