"""File xformer association

Revision ID: 7bffc2065a84
Revises: f6a49700f5d7
Create Date: 2024-08-13 20:59:12.922158

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import get_settings

db_type = "postgresql"
if "sqlite" in get_settings().db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "7bffc2065a84"
down_revision: Union[str, None] = "f6a49700f5d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "file_xformer_association",
        sa.Column("xformer_id", sa.String(48), nullable=False),
        sa.Column("file_id", sa.String(48), nullable=False, primary_key=True),
    )

    op.create_table(
        "file_manager",
        sa.Column("user_id", sa.String(48), nullable=False),
        sa.Column("file_id", sa.String(48), nullable=False),
        sa.Column("upload_id", sa.String(48), nullable=False),
        sa.Column("file_size", sa.Integer, nullable=False),
        sa.Column(
            "upload_date", sa.DateTime, nullable=False, default=sa.func.now()
        ),
    )

    op.create_index(
        "file_manager_user_id_index",
        "file_manager",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    pass
