from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models import User
from schemas import UserCreate, UserOut
from users.users import get_password_hash

router = APIRouter(prefix="/auth", tags=["Auth"])
session = get_session()


# Регистрация
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    summary="Регистрация пользователя",
)
async def register(
    data: UserCreate, db: Annotated[AsyncSession, Depends(get_session)]
) -> UserOut:
    result = await db.exec(select(User).where(User.username == data.username))
    db_user = result.first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(data.password)
    db_user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
