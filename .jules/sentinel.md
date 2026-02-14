# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Recurring PII Exposure in Patient Routes
**Vulnerability:** `patient_routes.py` endpoints exposed full PII/PHI without authentication, mirroring the user routes issue.
**Learning:** Developers are consistently forgetting security decorators on new resource modules. Manual review is insufficient.
**Prevention:** Implement automated tests that scan for missing `@require_auth` on all API routes, or use a "secure by default" middleware approach where public routes must be explicitly whitelisted.
