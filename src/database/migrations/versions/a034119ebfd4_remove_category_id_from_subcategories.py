"""Remove category_id from subcategories

Revision ID: a034119ebfd4
Revises: 7606d591d790
Create Date: 2024-01-27 17:52:57.821935

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a034119ebfd4'
down_revision = '7606d591d790'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subcategories', schema=None) as batch_op:
        batch_op.drop_constraint('subcategories_category_id_fkey', type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subcategories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.VARCHAR(length=26), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('subcategories_category_id_fkey', 'categories', ['category_id'], ['category_id'])

    # ### end Alembic commands ###
