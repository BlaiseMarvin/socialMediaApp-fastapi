"""add foreign-key to posts table

Revision ID: d6795c204c7b
Revises: 1bf3dd50e663
Create Date: 2022-03-18 11:30:48.290612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6795c204c7b'
down_revision = '1bf3dd50e663'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",
                            local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
