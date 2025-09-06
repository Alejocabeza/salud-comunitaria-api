"""empty message

Revision ID: a9b0403add79
Revises: eef02cd1c431
Create Date: 2025-09-05 20:15:40.607877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'a9b0403add79'
down_revision: Union[str, None] = 'eef02cd1c431'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
