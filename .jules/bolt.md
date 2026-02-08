## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-14 - Validated Index Performance
**Learning:** Confirmed via benchmarking that missing indexes on `Patient.caregiver_id` and `Appointment.patient_id` caused full table scans (~10ms). Adding `index=True` enabled index scans and reduced query time to ~0.85ms (12x improvement).
**Action:** Use `EXPLAIN QUERY PLAN` in local SQLite benchmarks to validate index usage before submitting performance fixes.
