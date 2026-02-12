## 2026-02-13 - Missing Indexes on Foreign Keys
**Learning:** SQLAlchemy models often lacked `index=True` on ForeignKey columns, even if the database migration (Alembic) created the index. This creates a potential for schema drift if models are used to generate migrations in the future. Additionally, some Foreign Keys (like `ReportModel.generated_by`) were missing indexes entirely in both code and DB.
**Action:** When adding or reviewing models, always verify that `ForeignKey` columns have `index=True` unless there is a specific reason not to index them. Check both the model definition and the migration file.

## 2026-02-13 - Regex Overhead in Hot Paths
**Learning:** `re.sub(r'\D', '', s)` is surprisingly slower than `''.join(filter(str.isdigit, s))` for short strings like CPF and Phone numbers. In value objects instantiated frequently (like thousands of Patients in a list), this regex compilation and execution adds measurable overhead.
**Action:** For simple character filtering (digits, alpha), prefer native string methods or `filter` over regex in hot paths. Also, avoid repeated type conversions (like `int(char)`) inside loops; convert once to a list of integers.
