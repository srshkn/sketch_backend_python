from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database.db import get_session
from src.database.models import User, UserOut
from src.users.models import CreateUser
from src.users.users import get_password_hash

router_user = APIRouter()
session = get_session()


# Регистрация
@router_user.post("/register", response_model=UserOut)
async def register(
    create_user: CreateUser, db: Annotated[Session, Depends(get_session)]
):
    result = await db.exec(select(User).where(User.username == create_user.username))
    db_user = result.first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(create_user.password)
    db_user = User(
        username=create_user.username,
        email=create_user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# Логин
@router_user.post("/token")
def login_for_access_token():
    pass


@router_user.get("/users/me")
def read_users_me():
    pass
