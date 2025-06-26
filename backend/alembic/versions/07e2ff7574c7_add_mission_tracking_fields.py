"""add mission tracking fields

Revision ID: 07e2ff7574c7
Revises: xxxxxxxxxxxx
Create Date: 2025-06-25 12:27:50.917449

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07e2ff7574c7'
down_revision: Union[str, Sequence[str], None] = 'xxxxxxxxxxxx'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE TYPE missionstatus AS ENUM ('pending', 'in_progress', 'completed', 'aborted')")
    op.add_column('drones', sa.Column('current_mission_id', sa.Integer(), sa.ForeignKey('missions.id'), nullable=True))
    op.add_column('missions', sa.Column('status', sa.Enum('pending', 'in_progress', 'paused', 'completed', 'aborted', name='missionstatus'), nullable=True, server_default='pending'))
    op.add_column('missions', sa.Column('started_at', sa.DateTime(), nullable=True))
    op.add_column('missions', sa.Column('ended_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('drones', 'current_mission_id')
    op.drop_column('missions', 'status')
    op.drop_column('missions', 'started_at')
    op.drop_column('missions', 'ended_at')
    op.execute("DROP TYPE IF EXISTS missionstatus")
