## 2025-02-17 - API Landing Page
**Learning:** For API-only projects, content negotiation at the root endpoint allows serving a friendly HTML landing page for developers (browser) while keeping JSON for programmatic access.
**Action:** Apply this pattern to all backend API services to improve onboarding and discoverability.

**Learning:** When using Flask's `request.accept_mimetypes.best_match`, the order of supported types matters for `*/*` clients. Always put the API default (JSON) before `text/html` to ensure `curl` and other tools get JSON by default, while browsers still get HTML.
