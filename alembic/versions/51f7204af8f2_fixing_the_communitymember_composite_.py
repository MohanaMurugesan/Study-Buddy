"""Fixing the communitymember composite primary key 
Revision ID: 51f7204af8f2
Revises: 
Create Date: 2025-09-03 12:39:24.605957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51f7204af8f2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint("community_members_pkey","community_members",type_="primary")

    op.create_primary_key(
        "community_members_pkey",
        "community_members",
        ["community_id","member_id"]
    )


def downgrade():
    op.drop_constraint("community_members_pkey", "community_members", type_="primary")

    op.create_primary_key("community_members_pkey", "community_members", ["community_id"])
