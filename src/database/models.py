from sqlmodel import Field, SQLModel


class UserOut(SQLModel):
    id: int
    user_name: str
    disable: bool


# Таблица пользователей
class User(UserOut, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=5, max_length=20)
    hashed_password: str
    disabled: bool = False
