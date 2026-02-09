"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from src.db import User, engine, get_session

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def session() -> AsyncSession:
    async with get_session() as s:
        yield s


@pytest.fixture(scope="module", autouse=True)
async def prepare_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def test_create_user(session: AsyncSession):
    user = User(username="testuser", hashed_password="hashed", disabled=False)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"


async def test_select_user(session: AsyncSession):
    result = await session.execute(select(User).where(User.username == "testuser"))
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.username == "testuser"
"""
