"""add comments

Revision ID: 14b7b6671936
Revises: 4518d718b2d8
Create Date: 2026-09-24 17:07:32.076458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14b7b6671936'
down_revision: Union[str, Sequence[str], None] = '4518d718b2d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
