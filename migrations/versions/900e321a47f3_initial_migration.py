"""Initial migration

Revision ID: 900e321a47f3
Revises: 
Create Date: 2025-02-10 17:23:55.009088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '900e321a47f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('skills', sa.PickleType(), nullable=True))
        batch_op.add_column(sa.Column('links', sa.PickleType(), nullable=True))
        batch_op.add_column(sa.Column('cv_path', sa.String(length=200), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('cv_path')
        batch_op.drop_column('links')
        batch_op.drop_column('skills')

    # ### end Alembic commands ###
