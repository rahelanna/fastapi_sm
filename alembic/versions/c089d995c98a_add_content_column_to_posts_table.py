"""add content column to posts table

Revision ID: c089d995c98a
Revises: cdcad3c251f3
Create Date: 2024-08-04 20:00:40.708135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c089d995c98a'
down_revision: Union[str, None] = 'cdcad3c251f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
