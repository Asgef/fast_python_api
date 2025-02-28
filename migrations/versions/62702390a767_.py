"""empty message

Revision ID: 62702390a767
Revises: ffa08c559168
Create Date: 2025-02-12 18:20:52.118083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62702390a767'
down_revision: Union[str, None] = 'ffa08c559168'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('logins', 'role',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('logins', 'role',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
