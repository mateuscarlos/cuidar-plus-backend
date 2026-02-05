## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2024-05-23 - Dark Mode & Emoji Accessibility in Backend Templates
**Learning:** Even simple backend landing pages can benefit significantly from "Micro-UX" improvements. Wrapping decorative emojis in `aria-hidden="true"` prevents screen reader clutter, and `prefers-color-scheme: dark` allows the page to respect system preferences with zero JavaScript.
**Action:** When creating default landing pages for APIs, always include a simple dark mode media query and ensure decorative icons are hidden from screen readers.
