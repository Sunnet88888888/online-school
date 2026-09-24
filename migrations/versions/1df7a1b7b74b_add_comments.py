"""add comments

Revision ID: 1df7a1b7b74b
Revises: 14b7b6671936
Create Date: 2026-09-24 17:08:50.859010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1df7a1b7b74b'
down_revision: Union[str, Sequence[str], None] = '14b7b6671936'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
