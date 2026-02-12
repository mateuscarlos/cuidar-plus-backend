# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Critical Auth Bypass in Middleware
**Vulnerability:** Authentication was completely bypassed when `FLASK_ENV` was set to "development", which is the default setting.
**Learning:** Default insecure configurations combined with environment-based bypasses create a high risk of accidental exposure in production.
**Prevention:** Remove environment-based security bypasses. Use valid credentials for development instead of bypassing checks.
