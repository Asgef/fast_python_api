"""empty message

Revision ID: cc4314b56766
Revises: f0332e119756
Create Date: 2025-02-18 14:16:28.597352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc4314b56766'
down_revision: Union[str, None] = 'f0332e119756'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('logins_uuid_fkey', 'logins', type_='foreignkey')
    op.create_foreign_key(None, 'logins', 'users', ['uuid'], ['id'], ondelete='CASCADE')
    op.drop_constraint('names_user_id_fkey', 'names', type_='foreignkey')
    op.create_foreign_key(None, 'names', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'names', type_='foreignkey')
    op.create_foreign_key('names_user_id_fkey', 'names', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'logins', type_='foreignkey')
    op.create_foreign_key('logins_uuid_fkey', 'logins', 'users', ['uuid'], ['id'])
    # ### end Alembic commands ###
