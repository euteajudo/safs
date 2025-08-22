"""merge_heads

Revision ID: af99e506b899
Revises: 123abc456def, a1b2c3d4e5f6
Create Date: 2025-08-20 14:12:04.707526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af99e506b899'
down_revision: Union[str, None] = ('123abc456def', 'a1b2c3d4e5f6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
