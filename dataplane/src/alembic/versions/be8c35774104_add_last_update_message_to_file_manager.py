"""add last update message to File manager

Revision ID: be8c35774104
Revises: bddc63a42567
Create Date: 2024-08-16 22:19:43.020945

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import get_settings

db_type = "postgresql"
if "sqlite" in get_settings().db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "be8c35774104"
down_revision: Union[str, None] = "bddc63a42567"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "file_manager",
        sa.Column("last_update_message", sa.String(), nullable=True),
    )


def downgrade() -> None:
    pass
