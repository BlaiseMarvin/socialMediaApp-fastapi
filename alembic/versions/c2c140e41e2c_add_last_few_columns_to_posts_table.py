"""add last few columns to posts table

Revision ID: c2c140e41e2c
Revises: d6795c204c7b
Create Date: 2022-03-18 11:53:31.692003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2c140e41e2c'
down_revision = 'd6795c204c7b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column(
        'published',sa.Boolean(),server_default='TRUE',nullable=False))
    op.add_column('posts',sa.Column(
        'created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
