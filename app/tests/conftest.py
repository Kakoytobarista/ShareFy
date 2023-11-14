import asyncio
from asyncio import current_task
from typing import AsyncGenerator, Iterator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_scoped_session, create_async_engine)
from sqlalchemy.orm import sessionmaker

from app.backend.session import get_db
from app.main import app
from app.models.v1.user import UserModel


@pytest_asyncio.fixture(scope="session")
async def async_db_connection() -> AsyncGenerator[AsyncConnection, None]:
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///", echo=False, connect_args={"timeout": 0.5}
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(UserModel.metadata.create_all)

    conn = await async_engine.connect()
    try:
        yield conn
    except Exception as e:
        raise e
    finally:
        await conn.rollback()

    async with async_engine.begin() as conn:
        await conn.run_sync(UserModel.metadata.drop_all)

    await async_engine.dispose()


async def __session_within_transaction(
        async_db_connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = sessionmaker(expire_on_commit=False,
                                       autocommit=False,
                                       autoflush=False,
                                       bind=async_db_connection,
                                       class_=AsyncSession)
    transaction = await async_db_connection.begin()

    yield async_scoped_session(async_session_maker, scopefunc=current_task)

    await transaction.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_db_session(
        async_db_connection: AsyncConnection,
) -> AsyncGenerator[AsyncSession, None]:
    async for session in __session_within_transaction(async_db_connection):
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client(async_db_session: AsyncSession) -> AsyncClient:
    """Set up the test client for the FastAPI app.

    Returns:
        AsyncClient: the async httpx test client to use in the tests.
    """

    def override_get_db() -> Iterator[AsyncSession]:
        """Utility function to wrap the database session in a generator.

        Yields:
            Iterator[AsyncSession]: An iterator containing one database session.
        """
        yield async_db_session

    app.dependency_overrides[get_db] = override_get_db
    return AsyncClient(app=app, base_url="http://test-server")


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
