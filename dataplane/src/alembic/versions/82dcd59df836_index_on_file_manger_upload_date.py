"""Index on file manger upload date

Revision ID: 82dcd59df836
Revises: c90856a7b91f
Create Date: 2024-08-16 22:50:58.791797

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import get_settings

db_type = "postgresql"
if "sqlite" in get_settings().db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "82dcd59df836"
down_revision: Union[str, None] = "c90856a7b91f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_file_manager_upload_date",
        "file_manager",
        ["upload_date"],
        unique=False,
    )


def downgrade() -> None:
    pass
