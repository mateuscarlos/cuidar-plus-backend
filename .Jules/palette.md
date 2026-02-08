## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2024-05-24 - Semantic Emojis in Links
**Learning:** Emojis in link text can be read verbosely by screen readers (e.g., "Page Facing Up API Documentation"), confusing the user.
**Action:** Wrap decorative emojis in `<span aria-hidden="true">` to ensure screen readers focus on the link label itself.

## 2024-05-24 - Dark Mode for Developer Tools
**Learning:** Even internal or API landing pages benefit from dark mode, as developers often work in dark environments.
**Action:** Use CSS custom properties and `@media (prefers-color-scheme: dark)` to easily add dark mode support without complex JS.
