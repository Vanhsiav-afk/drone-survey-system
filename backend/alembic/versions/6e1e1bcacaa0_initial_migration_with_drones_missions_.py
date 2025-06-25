"""initial migration with drones, missions, waypoints

Revision ID: 6e1e1bcacaa0
Revises: 
Create Date: 2025-06-24 16:47:28.247418

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

# revision identifiers, used by Alembic.
revision: str = 'xxxxxxxxxxxx'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Ensure PostGIS extension exists
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Create drones table
    op.create_table(
        'drones',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('battery_level', sa.Float(), nullable=False),
        sa.Column('status', sa.Enum('idle', 'in_mission', 'charging', name='dronestatus'), nullable=True),
        sa.Column('location', Geography(geometry_type='POINT', srid=4326), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create GIST index on location
    op.execute("""
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_class WHERE relname = 'idx_drones_location'
        ) THEN
            CREATE INDEX idx_drones_location ON drones USING gist (location);
        END IF;
    END
    $$;
    """)


    # Create missions table
    op.create_table(
        'missions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('altitude', sa.Float(), nullable=True),
        sa.Column('overlap_percentage', sa.Float(), nullable=True),
    )
    op.create_index(op.f('ix_missions_id'), 'missions', ['id'], unique=False)

    # Create waypoints table
    op.create_table(
        'waypoints',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('sequence', sa.Integer(), nullable=False),
        sa.Column('mission_id', sa.Integer(), sa.ForeignKey('missions.id'), nullable=True),
    )
    op.create_index(op.f('ix_waypoints_id'), 'waypoints', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_waypoints_id'), table_name='waypoints')
    op.drop_table('waypoints')

    op.drop_index(op.f('ix_missions_id'), table_name='missions')
    op.drop_table('missions')

    op.drop_index('idx_drones_location', table_name='drones')
    op.drop_table('drones')

    op.execute("DROP TYPE IF EXISTS dronestatus")