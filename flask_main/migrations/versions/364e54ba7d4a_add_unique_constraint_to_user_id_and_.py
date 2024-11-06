"""Add unique constraint to user_id and product_id in ProductUser

Revision ID: 364e54ba7d4a
Revises: d65d796f4f50
Create Date: 2024-11-06 08:42:20.644221

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '364e54ba7d4a'
down_revision = 'd65d796f4f50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_user', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.alter_column('product_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
        batch_op.drop_index('product_id')
        batch_op.drop_index('user_id')
        batch_op.drop_index('user_id_2')
        batch_op.create_unique_constraint('uix_user_product', ['user_id', 'product_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_user', schema=None) as batch_op:
        batch_op.drop_constraint('uix_user_product', type_='unique')
        batch_op.create_index('user_id_2', ['user_id'], unique=True)
        batch_op.create_index('user_id', ['user_id'], unique=True)
        batch_op.create_index('product_id', ['product_id'], unique=True)
        batch_op.alter_column('product_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###
