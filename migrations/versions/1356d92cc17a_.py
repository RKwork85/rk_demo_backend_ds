"""empty message

Revision ID: 1356d92cc17a
Revises: c52d0e66c0c2
Create Date: 2024-06-04 22:05:05.013975

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1356d92cc17a'
down_revision = 'c52d0e66c0c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###
