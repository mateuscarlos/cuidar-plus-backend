## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-14 - Patients Filtered by Caregiver Missing Index
**Learning:** Queries filtering `PatientModel` by `caregiver_id` were performing full table scans because `caregiver_id` (a Foreign Key) was not indexed. This was confirmed by `EXPLAIN QUERY PLAN` showing `SCAN patients`.
**Action:** Always ensure that Foreign Keys used in frequent WHERE clauses (like `list_by_parent`) are explicitly indexed with `index=True` in the SQLAlchemy model.
