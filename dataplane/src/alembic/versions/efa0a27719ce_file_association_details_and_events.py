"""File association details and events

Revision ID: efa0a27719ce
Revises: f22fd77e206e
Create Date: 2024-08-30 16:16:37.448515

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
revision: str = "efa0a27719ce"
down_revision: Union[str, None] = "f22fd77e206e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "file_xformer_association",
        sa.Column("assigned_to", sa.String(), nullable=True),
    )
    op.add_column(
        "file_xformer_association",
        sa.Column("failed_event_trigger_id", sa.String(), nullable=True),
    )
    op.add_column(
        "file_xformer_association",
        sa.Column("success_event_trigger_id", sa.String(), nullable=True),
    )
    op.create_table(
        "event_triggers",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(48), nullable=False),
        sa.Column("event_description", sa.String(), nullable=False),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("event_meta", sa.JSON(), nullable=False),
    )


def downgrade() -> None:
    pass
