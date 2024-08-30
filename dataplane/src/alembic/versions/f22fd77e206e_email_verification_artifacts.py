"""Email verification artifacts

Revision ID: f22fd77e206e
Revises: 82dcd59df836
Create Date: 2024-08-20 14:58:04.935115

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import get_settings

db_type = "postgresql"
if "sqlite" in get_settings().db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "f22fd77e206e"
down_revision: Union[str, None] = "82dcd59df836"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
