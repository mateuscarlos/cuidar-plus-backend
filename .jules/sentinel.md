# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Critical PII Exposure in Patient Routes
**Vulnerability:** `patient_routes.py` endpoints (`list_all_patients`, `create_patient`, `list_patients_by_caregiver`) were accessible without authentication, exposing PII.
**Learning:** New route files are prone to missing security decorators if not copy-pasted from a secured template or if the developer forgets to add them immediately.
**Prevention:** Implement a linter rule or a test that automatically checks for `@require_auth` on all routes in `src/presentation/api/v1/routes/` unless explicitly exempted.
