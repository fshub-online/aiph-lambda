"""added message priority

Revision ID: 880229bf3438
Revises: 376e04abf93d
Create Date: 2025-05-21 17:32:03.568913

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '880229bf3438'
down_revision: Union[str, None] = '376e04abf93d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the ENUM type first
    message_priority_enum = sa.Enum('Top', 'High', 'Medium', 'Low', name='messagepriority')
    message_priority_enum.create(op.get_bind())
    # Now add the column
    op.add_column('message', sa.Column('priority', sa.Enum('Top', 'High', 'Medium', 'Low', name='messagepriority'), nullable=False))

def downgrade() -> None:
    # Drop the column first
    op.drop_column('message', 'priority')
    # Then drop the ENUM type
    op.execute('DROP TYPE messagepriority')
