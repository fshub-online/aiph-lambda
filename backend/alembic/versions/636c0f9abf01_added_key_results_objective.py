"""added key-results, objective

Revision ID: 636c0f9abf01
Revises: 4cecd4ccd0a0
Create Date: 2025-05-22 18:02:22.010027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '636c0f9abf01'
down_revision: Union[str, None] = '4cecd4ccd0a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('objective',
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('priority', sa.Enum('low', 'medium', 'high', 'critical', name='objectivepriority'), nullable=False),
    sa.Column('status', sa.Enum('not_started', 'in_progress', 'at_risk', 'on_hold', 'delayed', 'completed', 'cancelled', name='objectivestatus'), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('measurable_target', sa.String(length=255), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['objective.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_objective_id'), 'objective', ['id'], unique=False)
    op.create_table('key_result',
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('objective_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('value_definition', sa.String(length=255), nullable=False),
    sa.Column('unit', sa.String(length=64), nullable=False),
    sa.Column('start_value', sa.Float(), nullable=False),
    sa.Column('current_value', sa.Float(), nullable=False),
    sa.Column('target_value', sa.Float(), nullable=False),
    sa.Column('status', sa.Enum('not_started', 'in_progress', 'at_risk', 'on_hold', 'delayed', 'completed', 'cancelled', 'current', 'planned', 'past', name='keyresultstatus'), nullable=False),
    sa.Column('priority', sa.Enum('low', 'medium', 'high', 'critical', name='keyresultpriority'), nullable=False),
    sa.Column('complexity', sa.Enum('trivial', 'easy', 'moderate', 'hard', 'extreme', name='keyresultcomplexity'), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.ForeignKeyConstraint(['objective_id'], ['objective.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_key_result_id'), 'key_result', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_key_result_id'), table_name='key_result')
    op.drop_table('key_result')
    op.drop_index(op.f('ix_objective_id'), table_name='objective')
    op.drop_table('objective')
    # ### end Alembic commands ###
