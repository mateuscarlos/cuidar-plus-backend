# Bolt's Journal

## 2024-05-22 - Missing Foreign Key Indexes
**Learning:** This codebase uses SQLAlchemy models where foreign keys (e.g., `caregiver_id` in `PatientModel`) are defined without explicit `index=True`. PostgreSQL does not automatically index foreign keys, which can lead to performance issues on joins and filtering by foreign key, specifically in `find_by_caregiver` queries.
**Action:** Always check for missing indexes on foreign key columns in `models/` when working on performance.

## 2024-05-22 - Repeated System Calls in Loops
**Learning:** Repeated calls to `date.today()` inside a list comprehension loop (e.g., calculating age for a list of patients) can cause significant overhead.
**Action:** Hoist system calls like `date.today()` outside of loops. Modifying entity methods to accept an optional `reference_date` allows for this optimization while maintaining testability and backward compatibility. Observed ~42% performance improvement in `ListPatientsByCaregiverUseCase`.
