# Bolt's Journal

## 2024-05-22 - Missing Foreign Key Indexes
**Learning:** This codebase uses SQLAlchemy models where foreign keys (e.g., `caregiver_id` in `PatientModel`) are defined without explicit `index=True`. PostgreSQL does not automatically index foreign keys, which can lead to performance issues on joins and filtering by foreign key, specifically in `find_by_caregiver` queries.
**Action:** Always check for missing indexes on foreign key columns in `models/` when working on performance.

## 2024-05-22 - Repeated System Calls in Loops
**Learning:** Repeated calls to `date.today()` inside a list comprehension loop (e.g., calculating age for a list of patients) can cause significant overhead.
**Action:** Hoist system calls like `date.today()` outside of loops. Modifying entity methods to accept an optional `reference_date` allows for this optimization while maintaining testability and backward compatibility. Observed ~42% performance improvement in `ListPatientsByCaregiverUseCase`.

## 2024-05-22 - N+1 Queries in Reports Summary
**Learning:** The reports summary endpoint was executing multiple independent `count()` queries (6 queries) for `Patient`, `Medication`, and `Appointment` statistics.
**Action:** Consolidate multiple count queries into a single query per table using conditional aggregation (e.g., `func.count(case((condition, column)))`). This reduced the number of queries from 6 to 3 and improved execution time by ~58% in benchmarks.

## 2024-05-22 - PostgreSQL ARRAY Type in SQLite Tests
**Learning:** Using `ARRAY` type in SQLAlchemy models breaks compatibility with SQLite (used for tests/benchmarks) as SQLite does not support arrays natively.
**Action:** Use `JSON().with_variant(ARRAY(Type), 'postgresql')` to allow using `JSON` storage in SQLite while preserving `ARRAY` behavior in PostgreSQL.
