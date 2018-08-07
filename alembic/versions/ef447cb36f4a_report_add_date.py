"""report add date

Revision ID: ef447cb36f4a
Revises: 19215a5c5cab
Create Date: 2018-08-07 17:44:04.474261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef447cb36f4a'
down_revision = '19215a5c5cab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('weekly_report', sa.Column('end_date', sa.DateTime(), nullable=True))
    op.add_column('weekly_report', sa.Column('start_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('weekly_report', 'start_date')
    op.drop_column('weekly_report', 'end_date')
    # ### end Alembic commands ###