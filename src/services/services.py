from db import DBManager


class UserService:
    def __init__(self, db: DBManager):
        self.db = db

    async def register(self, name: str, password: str):
        existing = await self.db.users.get_user_name(name)
        if existing:
            raise


class AuthServicesJWT:
    def __init__(self, db):
        self.db = db
