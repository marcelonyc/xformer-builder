from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Identity,
    Integer,
    MetaData,
    String,
    Table,
    Float,
    create_engine,
    VARCHAR,
    CursorResult,
    Select,
    Insert,
    Update,
    Delete,
    func,
)
from pydantic import PostgresDsn
from typing import Any
from sqlalchemy.dialects.postgresql import UUID, JSONB, BIGINT
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.asyncio import create_async_engine
from config.app_config import AppConfig
from constants import DB_NAMING_CONVENTION


app_config = AppConfig()

DATABASE_URL = str(app_config.db_url)
sync_db_url = DATABASE_URL.replace("+aiosqlite", "")
if "sqlite" in DATABASE_URL:
    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )
    engine_sync = create_engine(sync_db_url)
else:
    engine = create_async_engine(
        DATABASE_URL,
        pool_size=1,
        max_overflow=3,
        pool_pre_ping=True,
    )

    engine_sync = create_engine(
        sync_db_url,
        pool_size=1,
        max_overflow=3,
    )

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)


class XformerDB:
    def __init__(self, engine, engine_sync) -> None:
        self.engine = engine
        self.engine_sync = engine_sync

    async def fetch_one(
        self,
        select_query: Select,
    ) -> dict[str, Any] | None:
        async with self.engine.begin() as conn:
            cursor: CursorResult = await conn.execute(select_query)
            return cursor.first()._asdict() if cursor.rowcount > 0 else None

    async def fetch_all(
        self,
        select_query: Select,
    ) -> list[dict[str, Any]]:
        async with self.engine.begin() as conn:
            cursor: CursorResult = await conn.execute(select_query)
            return [r._asdict() for r in cursor.all()]

    def fetch_all_sync(
        self,
        select_query: Select,
    ) -> list[dict[str, Any]]:
        with self.engine_sync.begin() as conn:
            cursor: CursorResult = conn.execute(select_query)
            return [r._asdict() for r in cursor.all()]

    async def execute(self, select_query: Insert | Update | Delete) -> None:
        async with self.engine.begin() as conn:
            any_return = await conn.execute(select_query)
            return any_return

    def execute_sync(self, select_query: Insert | Update | Delete) -> None:
        with self.engine_sync.begin() as conn:
            any_return = conn.execute(select_query)
            return any_return

    async def disconnect(self) -> None:
        await self.engine.dispose()


database = XformerDB(engine, engine_sync)
# Database(
#     "{db_url}?application_name=application_pool".format(db_url=DATABASE_URL),
#     force_rollback=settings.ENVIRONMENT.is_testing,
# )

if "sqlite" in DATABASE_URL:
    json_type = JSON
else:
    json_type = JSONB

users = Table(
    "users",
    metadata,
    Column("token", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, nullable=False),
    Column("id", String, nullable=False),
    Column("description", String, nullable=False),
    Column("created_at", DateTime, nullable=False, default=func.now()),
    Column("updated_at", DateTime, nullable=False, default=func.now()),
    mustexist=False,
)

xformer_store = Table(
    "xformers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", String(48), nullable=False),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("xformer", json_type, nullable=False),
    Column("created_at", DateTime, nullable=False, default=func.now()),
)

file_xformer_association = Table(
    "file_xformer_association",
    metadata,
    Column("file_id", String(48), primary_key=False),
    Column("user_id", String(48), nullable=False),
    Column("description", String(100), nullable=True),
    Column("xformer_id", String(48), nullable=False),
)

file_manager = Table(
    "file_manager",
    metadata,
    Column("user_id", String(48), nullable=False),
    Column("file_id", String(48), nullable=False),
    Column("upload_id", String(48), nullable=False),
    Column("file_size", Integer, nullable=False),
    Column("upload_date", DateTime, nullable=False, default=func.now()),
    Column("last_update_message", String, nullable=True),
)