# Security Notes

Secrets stay in server-side environment variables. `.env` and SQLite files are ignored; `.env.example` has placeholders. `scripts/secret_scan.py` scans common key patterns. Prompt content and raw provider output logging are off by default.

React escapes user strings and uses no `dangerouslySetInnerHTML`. Inputs have length bounds. Local CORS allows only the Vite origin. Production deployments must add TLS, CSP, request-size and rate limits, strong authentication replacing the demo bearer token, secure secret storage, and retention controls.

