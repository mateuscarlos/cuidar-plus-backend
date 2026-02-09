## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2024-05-24 - Dark Mode and Screen Reader Noise
**Learning:** Simple HTML landing pages can support dark mode effectively using CSS variables and `@media (prefers-color-scheme: dark)`, improving visual comfort. Also, decorative emojis in buttons add unnecessary noise for screen readers.
**Action:** Use CSS variables for theming and wrap decorative emojis in `<span aria-hidden="true">`.
