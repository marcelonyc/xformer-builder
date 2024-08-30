"""File manager primary key

Revision ID: c90856a7b91f
Revises: be8c35774104
Create Date: 2024-08-16 22:26:42.282294

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import get_settings

db_type = "postgresql"
if "sqlite" in get_settings().db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "c90856a7b91f"
down_revision: Union[str, None] = "be8c35774104"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.batch_alter_table(
        "file_manager", recreate="always", copy_from="file_manager_temp"
    )
    with op.batch_alter_table("file_manager") as batch_op:
        batch_op.alter_column("file_id", nullable=False, primary_key=True)
        batch_op.alter_column("upload_id", nullable=False, primary_key=True)
        batch_op.create_index(
            "file_manager_file_id_upload_id_index",
            ["file_id", "upload_id"],
            unique=True,
        )
        batch_op.create_index(
            "file_manager_upload_id_file_id_index",
            ["upload_id", "file_id"],
            unique=True,
        )


def downgrade() -> None:
    pass
