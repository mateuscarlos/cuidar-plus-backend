"""Add index to appointments patient_id column

Revision ID: 003_add_index_to_appointments_patient_id
Revises: 002_add_index_to_reports_generated_by
Create Date: 2026-02-13 11:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '003_add_index_to_appointments_patient_id'
down_revision = '002_add_index_to_reports_generated_by'
depends_on = None


def upgrade():
    # Create index on patient_id column in appointments table
    op.create_index('ix_appointments_patient_id', 'appointments', ['patient_id'], unique=False)


def downgrade():
    # Drop index
    op.drop_index('ix_appointments_patient_id', table_name='appointments')
