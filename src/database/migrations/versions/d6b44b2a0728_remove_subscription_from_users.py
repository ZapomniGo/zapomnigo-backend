"""Remove subscription from users

Revision ID: d6b44b2a0728
Revises: 0eb316aeecec
Create Date: 2023-11-29 13:24:39.942395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6b44b2a0728'
down_revision = '0eb316aeecec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('users_subscription_model_id_fkey', type_='foreignkey')
        batch_op.drop_column('subscription_model_id')
        batch_op.drop_column('subscription_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subscription_date', sa.VARCHAR(length=40), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('subscription_model_id', sa.VARCHAR(length=26), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('users_subscription_model_id_fkey', 'subscription_models', ['subscription_model_id'], ['subscription_model_id'])

    # ### end Alembic commands ###
