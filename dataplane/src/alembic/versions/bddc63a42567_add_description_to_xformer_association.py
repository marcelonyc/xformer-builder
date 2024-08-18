"""Add description to xformer association

Revision ID: bddc63a42567
Revises: 5c2960930342
Create Date: 2024-08-16 15:12:28.030212

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
revision: str = "bddc63a42567"
down_revision: Union[str, None] = "5c2960930342"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "file_xformer_association",
        sa.Column("description", sa.String(100), nullable=True),
    )


def downgrade() -> None:
    pass
