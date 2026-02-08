# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2025-01-30 - Critical Auth Bypass in Patient Routes
**Vulnerability:** The `list_all_patients`, `create_patient`, and `list_patients_by_caregiver` endpoints in `patient_routes.py` were missing authentication checks.
**Learning:** Missing `@require_auth` on routes handling PII allows unauthorized access. This seems to be a recurring pattern.
**Prevention:** Audit all routes in `src/presentation/api/v1/routes/` to ensure `@require_auth` is applied to any route handling sensitive data.
