# Hospital ERP web client

This is the browser dashboard for the FastAPI service in `server/app.py`.

## Vercel settings

- Root Directory: `web`
- Framework Preset: Other
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment variable: `ERP_API_URL=https://<your-api-service>`

The API service must set `ERP_ALLOWED_ORIGINS` to the deployed Vercel URL. The
browser uses `/api/v1/auth/web-login`; all later requests use the short-lived
JWT returned by the API.
