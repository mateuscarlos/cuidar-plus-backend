"""Add index to reports generated_by column

Revision ID: 002_add_index_to_reports_generated_by
Revises: 001_add_new_modules
Create Date: 2026-02-13 10:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '002_add_index_to_reports_generated_by'
down_revision = '001_add_new_modules'
depends_on = None


def upgrade():
    # Create index on generated_by column in reports table
    op.create_index('ix_reports_generated_by', 'reports', ['generated_by'], unique=False)


def downgrade():
    # Drop index
    op.drop_index('ix_reports_generated_by', table_name='reports')
