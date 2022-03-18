"""create posts table

Revision ID: 3631e39b224e
Revises: 
Create Date: 2022-03-17 23:29:29.537287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3631e39b224e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
