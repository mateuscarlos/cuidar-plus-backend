## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-13 - Unindexed Foreign Key Performance Impact
**Learning:** Missing index on `AppointmentModel.patient_id` caused `SELECT` queries filtering by patient to be ~6x slower (0.008s vs 0.0013s in benchmark). This confirms that unindexed foreign keys are a significant bottleneck even with moderate dataset sizes (25k rows).
**Action:** Systematically audit all `ForeignKey` columns for `index=True`.
