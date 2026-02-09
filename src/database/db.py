from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
engine = create_async_engine(settings.DB_URL, echo=True)


async def get_session():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
