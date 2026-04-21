import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db import Base, get_session
from src.main import app

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:"
    f"{os.environ['POSTGRES_PASSWORD']}@"
    f"{os.environ['POSTGRES_SERVER']}:"
    f"{os.environ['POSTGRES_PORT']}/"
    f"{os.environ['POSTGRES_DB']}"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


async def truncate_tables(engine) -> None:
    tables = ", ".join(
        f'"{table.name}"' for table in reversed(Base.metadata.sorted_tables)
    )
    if not tables:
        return

    async with engine.begin() as conn:
        await conn.execute(text(f"TRUNCATE TABLE {tables} RESTART IDENTITY CASCADE;"))


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def clean_db(engine):
    await truncate_tables(engine)
    yield
    await truncate_tables(engine)


@pytest_asyncio.fixture
async def db_session(engine, clean_db):
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный HTTP-клиент, в котором реальная база данных
    подменена на тестовую.
    """

    # Функция для переопределения зависимости FastAPI
    def override_get_async_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_async_session

    # Используем ASGITransport для обхода необходимости поднимать реальный сервер
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as client:
        yield client

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()


@pytest.fixture
def valid_user_data() -> dict:
    """Фикстура с валидным payload для регистрации."""
    return {"name": "test_user", "password": "secure_password_123"}


@pytest.fixture
def another_user_data() -> dict:
    return {"name": "another_user", "password": "super_secure_456"}
