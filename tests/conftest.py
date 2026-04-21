import asyncio
import os
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
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

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Поднимает структуру БД (создает таблицы) перед каждым тестом
    и очищает их после завершения.
    """
    # Создаем все таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Отдаем сессию тесту
    async with TestingSessionLocal() as session:
        yield session

    # Удаляем таблицы после теста, обеспечивая чистоту для следующего
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


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
