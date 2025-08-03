"""Add gender column to users with default

Revision ID: 780c4b9ee616
Revises: 8e0e43b1d275
Create Date: 2025-08-03 12:01:42.858842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '780c4b9ee616'
down_revision: Union[str, Sequence[str], None] = '8e0e43b1d275'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
