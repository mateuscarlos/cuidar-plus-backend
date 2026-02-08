## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-14 - Schema Drift in Initial Migrations
**Learning:** `PatientModel.created_at` had `index=True` in the SQLAlchemy model, but the `000_initial_tables.py` migration did not create it. This caused schema drift where tests (using `create_all`) had the index, but production (using Alembic) did not.
**Action:** Do not trust SQLAlchemy model definitions alone for index existence. Always verify migration files. Tests using `create_all` may mask missing indexes in production.
