"""add raw token profile and hydrated pair payloads

Revision ID: ccf8ecc64082
Revises: 92d2b899be12
Create Date: 2026-09-04 14:33:20.452651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ccf8ecc64082"
down_revision: Union[str, Sequence[str], None] = "92d2b899be12"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "discoveries",
        sa.Column("token_profile", sa.JSON(), nullable=True),
    )
    op.add_column(
        "discoveries",
        sa.Column("pairs_data", sa.JSON(), nullable=True),
    )

    op.execute(
        sa.text(
            "UPDATE discoveries "
            "SET token_profile = '{}' "
            "WHERE token_profile IS NULL"
        )
    )
    op.execute(
        sa.text(
            "UPDATE discoveries "
            "SET pairs_data = '[]' "
            "WHERE pairs_data IS NULL"
        )
    )

    op.alter_column("discoveries", "token_profile", nullable=False)
    op.alter_column("discoveries", "pairs_data", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("discoveries", "pairs_data")
    op.drop_column("discoveries", "token_profile")
