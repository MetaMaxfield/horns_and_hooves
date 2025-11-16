"""initial

Создано вручную на основе предоставленных моделей. Эта миграция **создаёт только
таблицы приложения** и **не трогает** системные таблицы PostGIS.

Revision ID: 74fb13f0822f
Revises:
Create Date: 2025-11-16 00:08:30.387507
"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = "a4b4f1aee889"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema: create application tables only."""
    # --- activities ---
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["parent_id"], ["activities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- buildings ---
    op.create_table(
        "buildings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=200), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("geom", Geometry(geometry_type="POINT", srid=4326), nullable=False),
        sa.CheckConstraint(
            "latitude >= -90.0 AND latitude <= 90.0", name="latitude_range"
        ),
        sa.CheckConstraint(
            "longitude >= -180.0 AND longitude <= 180.0", name="longitude_range"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- organizations ---
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("building_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["building_id"], ["buildings.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- organization_activities (many-to-many) ---
    op.create_table(
        "organization_activities",
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["activity_id"], ["activities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("organization_id", "activity_id"),
    )

    # --- phone_numbers ---
    op.create_table(
        "phone_numbers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("num", sa.String(length=16), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organizations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema: drop application tables in reverse order."""
    # drop in reverse order to avoid FK issues
    op.drop_table("phone_numbers")
    op.drop_table("organization_activities")
    op.drop_table("organizations")
    op.drop_index("idx_buildings_geom", table_name="buildings")
    op.drop_table("buildings")
    op.drop_table("activities")
