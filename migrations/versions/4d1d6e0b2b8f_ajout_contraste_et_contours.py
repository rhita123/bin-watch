"""Ajout contraste et contours

Revision ID: 4d1d6e0b2b8f
Revises: cb91b3dc7527
Create Date: 2025-07-07 19:35:14.660040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d1d6e0b2b8f'
down_revision = 'cb91b3dc7527'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contrast', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('edge_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_column('edge_count')
        batch_op.drop_column('contrast')

    # ### end Alembic commands ###
