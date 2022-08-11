"""Added foreign key

Revision ID: 6b9bf3e5c5f2
Revises: 
Create Date: 2022-07-20 13:39:17.979582

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6b9bf3e5c5f2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts_table', sa.Column('poster_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts_table', 'register', ['poster_id'], ['id'])
    op.drop_column('posts_table', 'author_db')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts_table', sa.Column('author_db', mysql.VARCHAR(length=50), nullable=True))
    op.drop_constraint(None, 'posts_table', type_='foreignkey')
    op.drop_column('posts_table', 'poster_id')
    # ### end Alembic commands ###