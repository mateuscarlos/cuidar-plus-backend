## 2026-02-11 - Critical Vulnerability: Unauthenticated User Creation
**Vulnerability:** The `POST /api/v1/users/` endpoint was accessible without authentication, allowing any user to create new accounts, including those with 'admin' privileges.
**Learning:** This existed because the `create_user` endpoint lacked the `@require_auth` and `@require_role` decorators. Additionally, existing security tests (`tests/integration/test_user_routes_security.py`) were failing silently (or rather, testing the wrong thing) because they ran in the default environment where `FLASK_ENV` defaults to 'development' (or is not set to 'production'), triggering an authentication bypass in the middleware.
**Prevention:**
1. Always apply `@require_auth` to sensitive endpoints, especially those that modify state (POST/PUT/DELETE).
2. Ensure security tests explicitly mock `FLASK_ENV` to "production" to verify that authentication logic is actually enforced and not bypassed by development conveniences.
3. Review all endpoints for missing decorators during code reviews.
