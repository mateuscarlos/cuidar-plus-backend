"""Create insurers, providers, inventory_items and reports tables

Revision ID: 001_add_new_modules
Revises: 
Create Date: 2026-01-26

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_add_new_modules'
down_revision = None
depends_on = None


def upgrade():
    # Create insurers table
    op.create_table(
        'insurers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('trade_name', sa.String(255), nullable=False),
        sa.Column('cnpj', sa.String(14), unique=True, nullable=False, index=True),
        sa.Column('registration_number', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='ACTIVE'),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('address', postgresql.JSON, nullable=False),
        sa.Column('plans', postgresql.JSON, nullable=True),
        sa.Column('logo', sa.Text, nullable=True),
        sa.Column('contract_start_date', sa.DateTime, nullable=True),
        sa.Column('contract_end_date', sa.DateTime, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create inventory_items table
    op.create_table(
        'inventory_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('code', sa.String(50), unique=True, nullable=False, index=True),
        sa.Column('barcode', sa.String(100), unique=True, nullable=True, index=True),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('quantity', sa.Integer, nullable=False, server_default='0'),
        sa.Column('min_quantity', sa.Integer, nullable=False),
        sa.Column('max_quantity', sa.Integer, nullable=False),
        sa.Column('unit', sa.String(20), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='AVAILABLE'),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('batch', sa.String(100), nullable=True),
        sa.Column('expiration_date', sa.DateTime, nullable=True),
        sa.Column('supplier', sa.String(255), nullable=True),
        sa.Column('cost_price', sa.Float, nullable=False),
        sa.Column('sale_price', sa.Float, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create stock_movements table
    op.create_table(
        'stock_movements',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('item_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('reason', sa.Text, nullable=False),
        sa.Column('performed_by', sa.String(255), nullable=False),
        sa.Column('previous_quantity', sa.Integer, nullable=False),
        sa.Column('new_quantity', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create providers table
    op.create_table(
        'providers',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False, index=True),
        sa.Column('trade_name', sa.String(255), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING_APPROVAL'),
        sa.Column('document', sa.String(20), unique=True, nullable=False, index=True),
        sa.Column('credentials', postgresql.JSON, nullable=False),
        sa.Column('specialties', postgresql.JSON, nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('address', postgresql.JSON, nullable=False),
        sa.Column('working_hours', postgresql.JSON, nullable=True),
        sa.Column('services', postgresql.JSON, nullable=True),
        sa.Column('accepted_insurers', postgresql.JSON, nullable=True),
        sa.Column('logo', sa.Text, nullable=True),
        sa.Column('capacity', sa.Integer, nullable=True),
        sa.Column('has_emergency', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('rating', sa.Float, nullable=True),
        sa.Column('notes', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    
    # Create reports table
    op.create_table(
        'reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('type', sa.String(50), nullable=False, index=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('period', sa.String(50), nullable=False),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('end_date', sa.DateTime, nullable=False),
        sa.Column('format', sa.String(20), nullable=False),
        sa.Column('generated_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='PENDING', index=True),
        sa.Column('download_url', sa.Text, nullable=True),
        sa.Column('data', postgresql.JSON, nullable=True),
        sa.Column('error_message', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('completed_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('reports')
    op.drop_table('providers')
    op.drop_table('stock_movements')
    op.drop_table('inventory_items')
    op.drop_table('insurers')
