"""add user password

Revision ID: 17fbd11cf99b
Revises: 2846419352a7
Create Date: 2024-10-15 05:16:15.938622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '17fbd11cf99b'
down_revision: Union[str, None] = '2846419352a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('user', sa.Column('password', sa.Text, nullable=False))


def downgrade():
    op.drop_column('user', 'password')

