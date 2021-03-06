"""empty message

Revision ID: f4b48058aa9d
Revises: 8f2b1243a0a1
Create Date: 2019-11-19 10:30:23.098713

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f4b48058aa9d'
down_revision = '8f2b1243a0a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('comment', sa.String(length=100), nullable=True, comment='备注'))
    op.drop_column('product', 'commentd')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('commentd', mysql.VARCHAR(length=100), nullable=True, comment='备注'))
    op.drop_column('product', 'comment')
    # ### end Alembic commands ###
