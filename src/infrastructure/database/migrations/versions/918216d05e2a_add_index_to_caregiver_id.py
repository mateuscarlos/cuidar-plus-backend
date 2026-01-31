"""add_index_to_caregiver_id

Revision ID: 918216d05e2a
Revises:
Create Date: 2024-05-22 12:00:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '918216d05e2a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('ix_patients_caregiver_id', 'patients', ['caregiver_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_patients_caregiver_id', table_name='patients')
