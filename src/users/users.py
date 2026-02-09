from pydantic import BaseModel


class CreateUser(BaseModel):
    id: int
    user_name: str
    disable: bool
