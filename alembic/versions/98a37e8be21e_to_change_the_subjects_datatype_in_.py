"""To change the subjects datatype in profile table from jso to list

Revision ID: 98a37e8be21e
Revises: 018f5eb72b69
Create Date: 2025-09-06 10:49:59.008046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98a37e8be21e'
down_revision: Union[str, Sequence[str], None] = '018f5eb72b69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
