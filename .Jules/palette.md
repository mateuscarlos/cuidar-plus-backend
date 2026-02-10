## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2024-05-23 - Dark Mode and Decorative Emojis
**Learning:** Adding dark mode support via `@media (prefers-color-scheme: dark)` is a high-impact, low-effort way to improve user experience. Decorative emojis in UI elements must be hidden from screen readers using `aria-hidden="true"` to prevent noisy output.
**Action:** Always verify dark mode contrast and wrap decorative icons/emojis in aria-hidden spans.
