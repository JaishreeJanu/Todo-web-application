"""empty message

Revision ID: 2124b4a71df8
Revises: 9fb414ef4553
Create Date: 2020-03-21 12:22:34.032755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2124b4a71df8'
down_revision = '9fb414ef4553'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todolists', sa.Column('completed', sa.Boolean(), nullable=True))
    op.execute('UPDATE todolists SET completed = FALSE where completed IS NULL')
    op.alter_column('todolists','completed',nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todolists', 'completed')
    # ### end Alembic commands ###