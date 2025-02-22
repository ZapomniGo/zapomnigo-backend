"""Make confidence not null

Revision ID: 1adcdaaf35a3
Revises: bab471bd86b8
Create Date: 2024-01-13 17:36:52.790153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1adcdaaf35a3'
down_revision = 'bab471bd86b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews_flashcards', schema=None) as batch_op:
        batch_op.alter_column('confidence',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews_flashcards', schema=None) as batch_op:
        batch_op.alter_column('confidence',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
