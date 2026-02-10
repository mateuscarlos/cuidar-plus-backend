## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-13 - Performance Impact of Missing Model Indexes in Tests
**Learning:** When using `Base.metadata.create_all` for tests or local development (common with SQLite), the schema is derived directly from the models. If `index=True` is missing from `ForeignKey` columns in the models, the resulting tables will lack indexes, causing severe performance degradation (e.g., 17x slower queries in benchmarks) even if production migrations are correct.
**Action:** Always ensure `index=True` is present on `ForeignKey` columns in SQLAlchemy models to guarantee consistent performance across all environments (test, dev, prod), regardless of how the schema is created.
