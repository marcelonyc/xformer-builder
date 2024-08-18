"""Initialize DB

Revision ID: f6a49700f5d7
Revises: 
Create Date: 2024-08-03 11:23:50.561850

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON

from config.app_config import AppConfig

app_config = AppConfig()
db_type = "postgresql"
if "sqlite" in app_config.db_url:
    db_type = "sqlite"

# revision identifiers, used by Alembic.
revision: str = "f6a49700f5d7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if db_type == "sqlite":
        json_type = JSON
    else:
        json_type = JSONB

    op.create_table(
        "users",
        sa.Column("name", sa.String(100), nullable=False, primary_key=True),
        sa.Column("email", sa.String(60), nullable=False, primary_key=True),
        sa.Column("id", sa.String(100), nullable=False),
        sa.Column("token", sa.String(48), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime, nullable=False, default=sa.func.now()
        ),
    )
    op.create_table(
        "xformers",
        sa.Column("name", sa.String(100), primary_key=True),
        sa.Column("user_id", sa.String(48), primary_key=True),
        sa.Column("id", sa.String(48), nullable=False),
        sa.Column("description", sa.String(255), nullable=False),
        sa.Column("xformer", json_type, nullable=False),
        sa.Column(
            "created_at", sa.DateTime, nullable=False, default=sa.func.now()
        ),
    )

    with op.batch_alter_table("xformers") as batch_op:
        batch_op.create_foreign_key(
            "fk_xformers_users",
            "users",
            ["user_id"],
            ["id"],
        )

    op.create_index(
        "ix_xformers_user_id",
        "xformers",
        ["user_id", "name"],
    )
    op.create_index(
        "ix_users_token",
        "users",
        ["token"],
    )
    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
    )


def downgrade() -> None:
    pass
