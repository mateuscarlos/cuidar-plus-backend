# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Development Mode Authentication Bypass
**Vulnerability:** The `require_auth` and `require_role` decorators in `auth_middleware.py` completely bypassed authentication when `FLASK_ENV` was set to `development`. This risked exposing the entire application if deployed with the wrong environment variable.
**Learning:** Security logic should not have conditional bypasses based on environment variables, as this creates a "footgun" for deployment.
**Prevention:** Avoid conditional security logic. Use mock authentication providers in tests or development instead of bypassing the mechanism entirely.
