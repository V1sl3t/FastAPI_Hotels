"""add comforts

Revision ID: 7ac3d7cfdc3c
Revises: e1c75ffdede6
Create Date: 2024-10-05 08:22:47.538641

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7ac3d7cfdc3c"
down_revision: Union[str, None] = "e1c75ffdede6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comforts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "rooms_comforts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("comfort_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["comfort_id"],
            ["comforts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms_comforts")
    op.drop_table("comforts")
