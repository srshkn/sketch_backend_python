from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import create_db_and_tables
from routers import user_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_routers)


@app.get("/")
async def start():
    return {"message": "Hello World!"}
