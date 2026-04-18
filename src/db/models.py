from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserOut(SQLModel):
    id: int
    username: str
    disabled: bool


# Таблица пользователей
class User(UserOut, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=5, max_length=20)
    email: EmailStr = Field(index=True, unique=True, max_length=255)
    hashed_password: str
    disabled: bool = False
