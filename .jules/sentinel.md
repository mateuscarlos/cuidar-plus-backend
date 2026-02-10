# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2026-02-10 - Critical Auth Bypass in Patient Routes
**Vulnerability:** The `patient_routes.py` endpoints exposed full patient PII (CPF, address, etc.) without any authentication.
**Learning:** Security decorators must be manually applied to each route in this Flask Blueprint setup, making it easy to miss new endpoints.
**Prevention:** Consider implementing a global `before_request` hook for blueprints containing sensitive data, or using a linter rule to enforce `@require_auth` on routes in specific directories.
