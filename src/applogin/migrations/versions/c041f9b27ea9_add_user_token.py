"""add user token

Revision ID: c041f9b27ea9
Revises: 17fbd11cf99b
Create Date: 2024-10-16 02:21:25.389709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c041f9b27ea9'
down_revision: Union[str, None] = '17fbd11cf99b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('user', sa.Column('last_valid_token', sa.Text, nullable=True))


def downgrade():
    op.drop_column('user', 'last_valid_token')
