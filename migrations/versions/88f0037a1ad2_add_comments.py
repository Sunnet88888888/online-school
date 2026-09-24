"""add comments

Revision ID: 88f0037a1ad2
Revises: 4a402cc2e8b4
Create Date: 2026-09-24 17:12:27.202461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88f0037a1ad2'
down_revision: Union[str, Sequence[str], None] = '4a402cc2e8b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
