from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.сonfig import Config, load_config
from src.utils.utils import ENV_FILE

config: Config = load_config(ENV_FILE)
DATABASE_URL = config.databasesession.database_url
engine = create_async_engine(DATABASE_URL, echo=True)


class UserOut(SQLModel):
    id: int
    user_name: str
    disable: bool


class User(UserOut, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=5, max_length=20)
    hashed_password: str
    disabled: bool = False


async def get_session():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
