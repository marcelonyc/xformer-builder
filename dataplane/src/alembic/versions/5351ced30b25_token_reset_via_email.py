"""Token reset via email

Revision ID: 5351ced30b25
Revises: efa0a27719ce
Create Date: 2024-09-03 12:32:51.788870

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


from config.app_config import get_settings

app_config = get_settings()
db_type = "postgresql"
if "sqlite" in app_config.db_url:
    db_type = "sqlite"


# revision identifiers, used by Alembic.
revision: str = "5351ced30b25"
down_revision: Union[str, None] = "efa0a27719ce"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "password_reset",
        sa.Column("email", sa.String(60), nullable=False),
        sa.Column("reset_code", sa.String(100), nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=False),
    )

    op.batch_alter_table(
        "users",
        [
            sa.Column(
                "email",
                sa.String(60),
                nullable=False,
                primary_key=True,
                unique=True,
            ),
        ],
    )


def downgrade() -> None:
    pass
