"""empty message

Revision ID: 76b7004f6ffa
Revises: aaf2dcff354f
Create Date: 2019-12-16 15:39:08.953386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76b7004f6ffa'
down_revision = 'aaf2dcff354f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gongdan', sa.Column('explain', sa.TEXT(), nullable=True, comment='驳回说明'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('gongdan', 'explain')
    # ### end Alembic commands ###