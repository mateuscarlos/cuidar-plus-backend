## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2026-02-08 - Dark Mode Implementation Pattern
**Learning:** Simple HTML templates can support dark mode efficiently using CSS variables and a `@media (prefers-color-scheme: dark)` block within inline styles, eliminating the need for external CSS files.
**Action:** Use this inline CSS variable pattern for all standalone templates (e.g., error pages, landing pages) to ensure consistent theming.
