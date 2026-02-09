## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-13 - [Impact of Indexing Foreign Keys]
**Learning:** Adding `index=True` to `AppointmentModel.patient_id` improved query performance by ~24x (from 31ms to 1.3ms per query) in local benchmarks with 50k records. Foreign key columns used for filtering should always be indexed.
**Action:** Systematically review all foreign keys in models and ensure `index=True` is set where appropriate, especially for high-cardinality relationships like `patient_id`.
