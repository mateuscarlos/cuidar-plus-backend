# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Critical Auth Bypass in Patient Routes
**Vulnerability:** The `list_all_patients`, `create_patient`, and `list_patients_by_caregiver` endpoints in `patient_routes.py` were missing authentication checks, exposing PII.
**Learning:** The pattern of missing `@require_auth` decorators persisted in `patient_routes.py`, indicating a systemic issue where new routes default to insecure.
**Prevention:** Future work should implement a test that automatically scans all API routes and asserts they have `@require_auth` or an explicit exemption.
