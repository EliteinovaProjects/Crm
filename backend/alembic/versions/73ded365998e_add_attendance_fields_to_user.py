"""add_attendance_fields_to_user

Revision ID: 73ded365998e
Revises: 7cdabde502d3
Create Date: 2026-09-17 13:10:26.770331

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73ded365998e'
down_revision: Union[str, None] = '7cdabde502d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add attendance tracking fields to users table
    op.add_column('users', sa.Column('last_check_in', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_check_out', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('is_on_break', sa.Boolean(), nullable=True, server_default='false'))
    op.add_column('users', sa.Column('break_start_time', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('current_status', sa.String(), nullable=True, server_default='offline'))


def downgrade() -> None:
    # Remove attendance tracking fields from users table
    op.drop_column('users', 'current_status')
    op.drop_column('users', 'break_start_time')
    op.drop_column('users', 'is_on_break')
    op.drop_column('users', 'last_check_out')
    op.drop_column('users', 'last_check_in')
