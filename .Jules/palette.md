## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2026-02-11 - Dark Mode Implementation Pattern
**Learning:** Implementing dark mode in simple HTML templates can be achieved cleanly using CSS variables and `@media (prefers-color-scheme: dark)`. Overriding specific variables (`--bg-color`, `--text-color`, `--card-bg`, `--primary-color`) within the media query is sufficient without duplicate styles.
**Action:** Use CSS variables for all color definitions to enable easy theming and dark mode support with minimal code duplication.
