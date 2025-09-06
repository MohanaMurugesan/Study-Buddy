"""adding ondelete cascade to community_id in community_members

Revision ID: 018f5eb72b69
Revises: 51f7204af8f2
Create Date: 2025-09-03 13:13:40.195641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '018f5eb72b69'
down_revision: Union[str, Sequence[str], None] = '51f7204af8f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("community_members_community_id_fkey","community_members",type_="foreignkey")

    op.create_foreign_key(
        "community_members_community_id_fkey",
        "community_members",
        "community",
        ["community_id"],
        ["id"],
        ondelete="CASCADE"
    )

def downgrade() -> None:
    op.drop_constraint("community_members_community_id_fkey", "community_members", type_="foreignkey")

    op.create_foreign_key(
        "community_members_community_id_fkey",
        "community_members",
        "community",
        ["community_id"],
        ["id"]
    )