## 2026-01-31 - Missing Authentication on Sensitive Endpoints
**Vulnerability:** Found multiple sensitive API endpoints (`/patients`, `/inventory`, `/reports`) completely exposed to unauthenticated access. They returned PII (patient details, CPFs) without requiring a JWT token.
**Learning:** The project relies on explicit `@require_auth` decorators on each route handler. There is no "secure by default" mechanism at the Blueprint or App level. It's easy for developers to add new routes and forget the decorator.
**Prevention:** Consider implementing a `before_request` hook on the Blueprint level to enforce authentication for all routes within that blueprint, or implement an "Opt-out" authentication strategy (everything secure unless marked public).
