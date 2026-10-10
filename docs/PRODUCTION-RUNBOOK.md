# Production Runbook

## Start
1. Load secrets from the approved secret store/environment.
2. Verify TLS certificate and hostname.
3. Verify PostgreSQL connectivity.
4. Verify Redis/session service if enabled.
5. Run health checks.
6. Run backup-status check.
7. Start API behind Nginx/load balancer.

## Stop / rollback
- Drain client traffic.
- Stop application containers/services.
- Preserve logs.
- Roll back application image/configuration.
- Restore database only when required and approved.
- Re-run health/UAT smoke tests.

## Never
- Do not place production secrets in source control.
- Do not copy production patient data into developer/test environments.
- Do not claim a penetration test or compliance approval without an external report/sign-off.
