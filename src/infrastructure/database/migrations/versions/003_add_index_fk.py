"""Add index to foreign keys in appointments and patients tables

Revision ID: 003_add_index_fk
Revises: 002_add_index_to_reports_generated_by
Create Date: 2026-02-14 10:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '003_add_index_fk'
down_revision = '002_add_index_to_reports_generated_by'
depends_on = None


def upgrade():
    # Create index on patient_id column in appointments table
    op.create_index('ix_appointments_patient_id', 'appointments', ['patient_id'], unique=False)
    # Create index on caregiver_id column in patients table
    op.create_index('ix_patients_caregiver_id', 'patients', ['caregiver_id'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_appointments_patient_id', table_name='appointments')
    op.drop_index('ix_patients_caregiver_id', table_name='patients')
