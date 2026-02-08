"""Add index to patients created_at column

Revision ID: 003_add_index_to_patients_created_at
Revises: 002_add_index_to_reports_generated_by
Create Date: 2026-02-14 10:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '003_add_index_to_patients_created_at'
down_revision = '002_add_index_to_reports_generated_by'
depends_on = None


def upgrade():
    # Create index on created_at column in patients table
    op.create_index('ix_patients_created_at', 'patients', ['created_at'], unique=False)


def downgrade():
    # Drop index
    op.drop_index('ix_patients_created_at', table_name='patients')
