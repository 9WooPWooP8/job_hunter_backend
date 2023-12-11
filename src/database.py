from typing import Annotated, Any

from sqlalchemy import CursorResult, Insert, MetaData, Select, Update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings
from src.constants import DB_NAMING_CONVENTION

DATABASE_URL = str(settings.DATABASE_URL)

engine = create_async_engine(DATABASE_URL)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    try:
        db_session = session_maker()
        yield db_session
    finally:
        await db_session.close()


GetDB = Annotated[AsyncSession, get_db]


async def fetch_one(
    session: AsyncSession, select_query: Select | Insert | Update
) -> dict[str, Any] | None:
    cursor: CursorResult = await session.execute(select_query)
    return cursor.unique().scalars().one_or_none()


async def fetch_all(
    session: AsyncSession, select_query: Select | Insert | Update
) -> list[dict[str, Any]]:
    cursor: CursorResult = await session.execute(select_query)
    return cursor.unique().scalars().all()


async def execute(session: AsyncSession, select_query: Insert | Update) -> None:
    await session.execute(select_query)
