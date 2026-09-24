"""add comments

Revision ID: 4a402cc2e8b4
Revises: 1df7a1b7b74b
Create Date: 2026-09-24 17:09:38.364110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a402cc2e8b4'
down_revision: Union[str, Sequence[str], None] = '1df7a1b7b74b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
