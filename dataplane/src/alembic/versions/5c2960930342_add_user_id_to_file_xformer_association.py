"""Add user_id to file_xformer_association

Revision ID: 5c2960930342
Revises: 7bffc2065a84
Create Date: 2024-08-14 20:49:54.721437

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import AppConfig

app_config = AppConfig()
db_type = "postgresql"
if "sqlite" in app_config.db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "5c2960930342"
down_revision: Union[str, None] = "7bffc2065a84"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "file_xformer_association",
        sa.Column("user_id", sa.String(48), nullable=False),
    )
    op.create_index(
        "file_xformer_association_user_id_index",
        "file_xformer_association",
        ["user_id"],
    )
    pass


def downgrade() -> None:
    pass
