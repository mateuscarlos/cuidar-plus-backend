# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2026-02-07 - Critical Auth Bypass in Patient Routes
**Vulnerability:** The `list_all_patients`, `create_patient`, and `list_patients_by_caregiver` endpoints in `patient_routes.py` were missing authentication checks, exposing sensitive PII.
**Learning:** Routes defined in Blueprints do not inherit protection unless explicitly applied or enforced by global middleware.
**Prevention:** Mandate security integration tests that specifically target unauthenticated access for all new endpoints.
