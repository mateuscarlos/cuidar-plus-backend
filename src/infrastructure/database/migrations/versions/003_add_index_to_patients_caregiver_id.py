"""Add index to patients caregiver_id column

Revision ID: 003_add_index_to_patients_caregiver_id
Revises: 002_add_index_to_reports_generated_by
Create Date: 2026-02-14 14:30:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '003_add_index_to_patients_caregiver_id'
down_revision = '002_add_index_to_reports_generated_by'
depends_on = None


def upgrade():
    # Create index on caregiver_id column in patients table
    op.create_index('ix_patients_caregiver_id', 'patients', ['caregiver_id'], unique=False)


def downgrade():
    # Drop index
    op.drop_index('ix_patients_caregiver_id', table_name='patients')
