from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from db import SessionLocal
from repositories import AuthRepository, UserRepository


class DBManager:
    def __init__(self, session_factory: Callable[[], AsyncSession] = SessionLocal):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self.users: UserRepository | None = None
        self.auth: AuthRepository | None = None
