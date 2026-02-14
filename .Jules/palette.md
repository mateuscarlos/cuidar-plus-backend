## 2024-05-23 - Accessibility in API Landing Pages
**Learning:** Even simple API landing pages need accessible contrast ratios. Buttons using standard "nice blue" (#3498db) often fail WCAG AA for white text.
**Action:** Always check contrast ratios for buttons. Use darker blues like #1e6bb8 for better accessibility.

## 2024-05-23 - SQLAlchemy SQLite Compatibility
**Learning:** SQLAlchemy's `create_engine` throws TypeError if `pool_size` or `max_overflow` are passed when using SQLite, unlike Postgres.
**Action:** When configuring database connections in a mixed environment (Postgres prod / SQLite test), filter out pool arguments for SQLite.

## 2025-02-14 - Decorative Emojis Accessibility
**Learning:** Decorative emojis in UI text (like buttons) can be verbose or confusing for screen readers (e.g., "Page facing up" vs just "API Documentation").
**Action:** Always wrap purely decorative emojis in an element with `aria-hidden="true"`.

## 2025-02-14 - Dark Mode in Single-File Templates
**Learning:** For simple landing pages without a CSS preprocessor, extracting all hardcoded colors to CSS variables in `:root` makes adding dark mode support trivial via media query overrides.
**Action:** Use CSS variables for all colors from the start, even in simple prototypes.
