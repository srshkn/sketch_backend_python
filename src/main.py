from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.db import create_db_and_tables
from src.users.users_routers import router_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router_user)


@app.get("/")
async def start():
    return {"message": "Hello World!"}
