from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import User
from schemas import UserCreate, UserOut
from users.users import get_password_hash

router = APIRouter()
session = get_session()


# Регистрация
@router.post("/register", response_model=UserOut)
async def register(
    create_user: UserCreate, db: Annotated[Session, Depends(get_session)]
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
@router.post("/token")
def login_for_access_token():
    pass


@router.get("/users/me")
def read_users_me():
    pass
