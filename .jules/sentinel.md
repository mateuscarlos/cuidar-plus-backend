## 2025-02-12 - Missing Authentication on Sensitive Endpoints
**Vulnerability:** The `list_users` and `get_user` endpoints in `user_routes.py` were completely publicly accessible, exposing sensitive user data (including PII like emails, full names, roles, and status).
**Learning:** The project relies on manual application of `@require_auth` decorator on each route, instead of a secure-by-default global middleware approach. This makes it easy to accidentally expose new endpoints if the developer forgets the decorator.
**Prevention:** Implement a global middleware or a "secure by default" router wrapper that requires authentication unless explicitly exempted (allow-list approach). For now, always check for `@require_auth` when reviewing new routes.
