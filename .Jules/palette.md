## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2025-02-07 - Decorative Emojis Accessibility
**Learning:** Decorative emojis in links (e.g., "📄 API Documentation") can be verbose or confusing for screen readers if not hidden.
**Action:** Wrap decorative emojis in `<span aria-hidden="true">` to ensure they are visual-only.
