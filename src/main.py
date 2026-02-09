from fastapi import FastAPI

from src.users.users_routers import router_user

app = FastAPI()

app.include_router(router_user)


@app.get("/")
async def start():
    return {"message": "Hello World!"}
