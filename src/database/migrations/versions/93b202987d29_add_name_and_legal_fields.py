"""Add name and legal fields

Revision ID: 93b202987d29
Revises: c26632f56a68
Create Date: 2023-11-07 00:00:53.351667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93b202987d29'
down_revision = 'c26632f56a68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=40), nullable=False))
        batch_op.add_column(sa.Column('privacy_policy', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('terms_and_conditions', sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column('marketing_consent', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('marketing_consent')
        batch_op.drop_column('terms_and_conditions')
        batch_op.drop_column('privacy_policy')
        batch_op.drop_column('name')

    # ### end Alembic commands ###
