# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Critical PII Exposure in Patient Routes
**Vulnerability:** The patient management endpoints (`/api/v1/patients/`) were completely unprotected, exposing sensitive PII and medical data.
**Learning:** Routes created using `Blueprint` without a global auth policy must explicitly apply security decorators to each handler.
**Prevention:** Implement a default-deny policy for API blueprints or use a linter rule to flag public routes returning PII.
