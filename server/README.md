# Phase 4 Secure Server Layer

The hospital desktop client should call this API instead of carrying the central database and AI provider secret locally.

## Windows developer setup

1. Create a server-only `.env` from `.env.server.example`.
2. Set a strong `ERP_API_KEY`.
3. Install `requirements-server.txt`.
4. Run behind a TLS-enabled reverse proxy for production.

The sample API deliberately exposes only small, approved endpoints. Expand it only with role-checked service methods; never expose arbitrary SQL.
