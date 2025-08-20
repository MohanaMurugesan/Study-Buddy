"""updated the token and requested_time column to not null

Revision ID: 3d67c07e8b2d
Revises: 3b8310b16a3e
Create Date: 2025-08-19 11:11:35.129892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d67c07e8b2d'
down_revision: Union[str, Sequence[str], None] = '3b8310b16a3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("otps","token",existing_type=sa.String,nullable=False)
    op.alter_column("otps","last_requested_time",existing_type=sa.TIMESTAMP(timezone=True),nullable=False)

def downgrade() -> None:
    op.alter_column("otps","token",existing_type=sa.String,nullable=True)
    op.alter_column("otps","last_requested_time",existing_type=sa.TIMESTAMP(timezone=True),nullable=True)
