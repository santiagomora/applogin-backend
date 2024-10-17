"""create user table

Revision ID: 2846419352a7
Revises: 
Create Date: 2024-10-15 03:24:02.891693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2846419352a7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('name', sa.Text, nullable=False),
                    sa.Column('lastname', sa.Text, nullable=False),
                    sa.Column('email', sa.Text, unique=True),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              nullable=False,
                              server_default=sa.sql.func.now()))


def downgrade():
    op.drop_table('user')
