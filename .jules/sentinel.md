# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2026-02-08 - Critical Auth Bypass in Patient Routes
**Vulnerability:** The `list_all_patients`, `create_patient`, and `list_patients_by_caregiver` endpoints in `patient_routes.py` were missing authentication checks.
**Learning:** Copy-pasting blueprints without verifying security decorators is a common source of vulnerabilities.
**Prevention:** Implement a linter rule or automated test that checks for `@require_auth` on all routes in `src/presentation/api/v1/routes/`.
