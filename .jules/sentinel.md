# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2024-05-24 - Critical PII Exposure in Patient Routes
**Vulnerability:** The `patient_routes.py` endpoints (`list_all_patients`, `create_patient`, `list_patients_by_caregiver`) were completely public, exposing sensitive PII (CPF, Health data, Contact info).
**Learning:** Adding new resources/routes often leads to copy-pasting structure but forgetting security decorators if they aren't enforced by default or by a linter. The "default open" nature of Flask routes requires vigilance.
**Prevention:** Implement a linter rule or a test that fails if a route in `api/v1` does not have `@require_auth` or an explicit `@public` decorator (if we create one).
