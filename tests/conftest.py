import asyncio
from typing import AsyncGenerator, Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)

from src.main import app
from src.core.models import Base
from src.core.config import settings


@pytest.fixture(scope="session")
def async_engine() -> AsyncEngine:
    _async_engine: AsyncEngine = create_async_engine(
        url=settings.postgres_settings.get_pg_url(),
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    )
    return _async_engine


@pytest.fixture(scope="session")
def async_session_maker(async_engine) -> async_sessionmaker:
    _async_session_maker: async_sessionmaker = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return _async_session_maker


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def make_db(async_engine) -> AsyncGenerator:
    assert settings.MODE == 'TEST'
    async with async_engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.drop_all)
        await db_conn.run_sync(Base.metadata.create_all)
    # yield
    # async with async_engine.begin() as db_conn:
    #     await db_conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_session(async_session_maker) -> AsyncGenerator:
    async with async_session_maker() as _async_session:
        yield _async_session


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c