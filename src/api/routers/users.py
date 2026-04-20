from fastapi import APIRouter, HTTPException, status

from api import DBManagerDep
from core.exceptions import AppError, UserAlreadyExistsError
from db import get_session
from schemas import UserCreate, UserOut
from services import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])
session = get_session()


# Регистрация
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
    summary="Регистрация пользователя",
)
async def register(data: UserCreate, db: DBManagerDep) -> UserOut:
    service = UserService()
    try:
        return await service.register(data.name, data.password)
    except UserAlreadyExistsError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="") from err
    except AppError as err:
        detail = str(err) or ""
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        ) from err
