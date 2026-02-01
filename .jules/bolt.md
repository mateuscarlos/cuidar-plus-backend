## 2026-01-28 - Optimized Reports Summary
**Learning:** SQLite does not support `ARRAY` type which caused test failures. Used `JSON().with_variant(ARRAY(Time), 'postgresql')` to support both SQLite (for tests) and PostgreSQL (production).
**Action:** Use `with_variant` for dialect-specific types when writing models.

**Learning:** Reducing database round trips by aggregating multiple counts into a single query using `func.count` and `case` is a simple and effective optimization for summary endpoints.
**Action:** Look for sequential `count()` queries and aggregate them.
