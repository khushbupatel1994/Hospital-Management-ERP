# Phase 11 Pilot Release Gate

## Automated engineering gates
- [ ] Python compilation passes
- [ ] Unit/integration tests pass
- [ ] Release manifest hash verification passes
- [ ] Production environment preflight passes
- [ ] Database migration preflight passes
- [ ] Backup integrity check passes
- [ ] Restore drill passes in an isolated environment
- [ ] API health smoke test passes

## External gates (must be signed by the responsible party)
- [ ] Independent penetration test completed and critical/high findings remediated
- [ ] Hospital UAT completed and signed
- [ ] Privacy/legal/compliance review completed
- [ ] TLS certificate issued and installed
- [ ] Code-signing certificate issued and Windows release signed
- [ ] Production server/network/firewall approved
- [ ] Backup retention and disaster-recovery targets approved
- [ ] Incident-response contacts approved

## Pilot rollback
1. Stop new client deployments.
2. Preserve audit and application logs.
3. Disable the affected feature/API route if needed.
4. Restore the last verified database backup in the recovery environment.
5. Validate critical workflows.
6. Re-enable service only after incident owner approval.
