"""add content column to posts table

Revision ID: 67bb59ffa078
Revises: 3631e39b224e
Create Date: 2022-03-18 10:56:16.646871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bb59ffa078'
down_revision = '3631e39b224e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))


def downgrade():
    op.drop_column('posts','content')
    
