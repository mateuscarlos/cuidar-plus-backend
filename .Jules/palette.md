## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2026-02-04 - Seamless Dark Mode with CSS Variables
**Learning:** Using CSS variables for colors (e.g., `--bg-color`, `--text-color`) allows for "invisible" dark mode implementation via `@media (prefers-color-scheme: dark)` without requiring JavaScript or complex class toggling.
**Action:** Define all color primitives as CSS variables in `:root` and override them in the media query for instant, flicker-free dark mode support.
