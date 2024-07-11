"""Fix groups relations

Revision ID: 1baec5cfc5d3
Revises: 62ddb877ff86
Create Date: 2024-07-11 16:23:55.957511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1baec5cfc5d3'
down_revision: Union[str, None] = '62ddb877ff86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event_type', sa.Column('group_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'event_type', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'event_type', type_='foreignkey')
    op.drop_column('event_type', 'group_id')
    # ### end Alembic commands ###
