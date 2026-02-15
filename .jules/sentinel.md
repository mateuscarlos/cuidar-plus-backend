# Sentinel's Journal

## 2024-05-23 - Critical Auth Bypass in User Routes
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were missing authentication checks.
**Learning:** Even with a clean architecture, missing decorators on the presentation layer can expose sensitive data.
**Prevention:** Always verify that route handlers dealing with sensitive data (PII) have `@require_auth` applied.

## 2025-01-28 - Systemic Missing Auth on PII Endpoints
**Vulnerability:** The `patient_routes.py` (and others like `inventory_routes.py`) endpoints were completely unprotected, exposing PII.
**Learning:** The previous fix in `user_routes.py` was not applied systematically. Manual decoration is prone to human error.
**Prevention:** In the future, consider a middleware that enforces authentication by default for all `/api/` routes, requiring an explicit `@public` decorator for exceptions.
