import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from redis.asyncio import Redis

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
from database.base import Base
from database.connection import get_db
from redis_client.redis_client import get_redis



BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

if os.path.exists(f"{BASE_DIR}/data/test_database.db"):
    os.remove(f"{BASE_DIR}/data/test_database.db")

TEST_DATABASE_URL = f"sqlite+aiosqlite:///{DATA_DIR}/test_database.db"

engine_test = create_async_engine(TEST_DATABASE_URL)

async_session_maker = async_sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)



@pytest_asyncio.fixture
async def test_redis():
    """
    Подключается к отдельной Redis DB для тестов.
    Использует Redis на localhost:6379, DB 15.
    """

    redis = Redis(
        host="localhost",
        port=6379,
        db=15,
        decode_responses=True,
    )

    await redis.ping()

    await redis.flushdb()

    yield redis

    await redis.flushdb()
    await redis.aclose()



@pytest_asyncio.fixture(autouse=True)
async def setup_test_database():
    """Создаёт таблицы перед тестом."""

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # При необходимости можно удалять таблицы после каждого теста:
    # async with engine_test.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)




@pytest_asyncio.fixture
async def client(test_redis):
    """
    Создаёт тестовый HTTP-клиент.
    Подменяет зависимости БД и Redis.
    """

    async def override_get_db():
        async with async_session_maker() as session:
            yield session

    def override_get_redis():
        return test_redis

    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac

    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)



@pytest_asyncio.fixture(autouse=True)
async def dispose_test_engine():
    yield
    await engine_test.dispose()