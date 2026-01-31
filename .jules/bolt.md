# Bolt's Journal

## 2024-05-22 - Missing Foreign Key Indexes
**Learning:** This codebase uses SQLAlchemy models where foreign keys (e.g., `caregiver_id` in `PatientModel`) are defined without explicit `index=True`. PostgreSQL does not automatically index foreign keys, which can lead to performance issues on joins and filtering by foreign key, specifically in `find_by_caregiver` queries.
**Action:** Always check for missing indexes on foreign key columns in `models/` when working on performance.
