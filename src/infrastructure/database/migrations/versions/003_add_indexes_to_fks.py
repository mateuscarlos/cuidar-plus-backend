"""Add indexes to foreign keys

Revision ID: 003_add_indexes_to_fks
Revises: 002_add_index_to_reports_generated_by
Create Date: 2026-02-14 10:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '003_add_indexes_to_fks'
down_revision = '002_add_index_to_reports_generated_by'
depends_on = None


def upgrade():
    # Create index on caregiver_id in patients table
    op.create_index('ix_patients_caregiver_id', 'patients', ['caregiver_id'], unique=False)

    # Create index on patient_id in appointments table
    op.create_index('ix_appointments_patient_id', 'appointments', ['patient_id'], unique=False)

    # Create index on patient_id in medications table
    op.create_index('ix_medications_patient_id', 'medications', ['patient_id'], unique=False)


def downgrade():
    # Drop indexes
    op.drop_index('ix_medications_patient_id', table_name='medications')
    op.drop_index('ix_appointments_patient_id', table_name='appointments')
    op.drop_index('ix_patients_caregiver_id', table_name='patients')
