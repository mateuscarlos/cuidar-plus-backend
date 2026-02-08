# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Unauthenticated Patient Data Exposure
**Vulnerability:** The `patient_routes.py` endpoints exposed sensitive PII (CPF, address, medical info) without authentication. Also leaked exception details in error responses.
**Learning:** Copy-pasting route patterns without checking for `@require_auth` propagates security holes. Exception handling returning `str(e)` is a common leak pattern.
**Prevention:** Enforce `@require_auth` on all PII routes by default. Use generic error messages for 500 responses.
