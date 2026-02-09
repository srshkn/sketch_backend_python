from fastapi import APIRouter

router_user = APIRouter()


# Регистрация
@router_user.post("/register")
def register():
    pass


# Логин
@router_user.post("/token")
def login_for_access_token():
    pass


@router_user.get("/users/me")
def read_users_me():
    pass
