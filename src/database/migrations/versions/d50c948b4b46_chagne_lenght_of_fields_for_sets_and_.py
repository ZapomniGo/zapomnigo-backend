"""Chagne lenght of fields for sets and flashcards

Revision ID: d50c948b4b46
Revises: c9f2de05c161
Create Date: 2023-12-26 22:14:20.744313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd50c948b4b46'
down_revision = 'c9f2de05c161'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('flashcards', schema=None) as batch_op:
        batch_op.alter_column('term',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=16384),
               existing_nullable=False)
        batch_op.alter_column('definition',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=16384),
               existing_nullable=False)
        batch_op.alter_column('notes',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=16384),
               existing_nullable=True)

    with op.batch_alter_table('sets', schema=None) as batch_op:
        batch_op.alter_column('set_name',
               existing_type=sa.VARCHAR(length=40),
               type_=sa.String(length=255),
               existing_nullable=False)
        batch_op.alter_column('set_description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=4096),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sets', schema=None) as batch_op:
        batch_op.alter_column('set_description',
               existing_type=sa.String(length=4096),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.alter_column('set_name',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False)

    with op.batch_alter_table('flashcards', schema=None) as batch_op:
        batch_op.alter_column('notes',
               existing_type=sa.String(length=16384),
               type_=sa.VARCHAR(length=255),
               existing_nullable=True)
        batch_op.alter_column('definition',
               existing_type=sa.String(length=16384),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
        batch_op.alter_column('term',
               existing_type=sa.String(length=16384),
               type_=sa.VARCHAR(length=40),
               existing_nullable=False)

    # ### end Alembic commands ###
