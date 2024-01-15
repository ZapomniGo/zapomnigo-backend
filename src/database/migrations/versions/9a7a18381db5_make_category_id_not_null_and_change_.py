"""make category_id not null and change fields length

Revision ID: 9a7a18381db5
Revises: 3578d955cce0
Create Date: 2024-01-14 19:50:03.091921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a7a18381db5'
down_revision = '3578d955cce0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folders', schema=None) as batch_op:
        batch_op.alter_column('folder_title',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('folder_description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=4096),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('folders', schema=None) as batch_op:
        batch_op.alter_column('folder_description',
               existing_type=sa.String(length=4096),
               type_=sa.VARCHAR(length=255),
               nullable=False)
        batch_op.alter_column('folder_title',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False)

    # ### end Alembic commands ###
