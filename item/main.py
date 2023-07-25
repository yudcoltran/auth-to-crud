from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values
from contextlib import asynccontextmanager
from .routers import user, item, authen

config = dotenv_values()

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = MongoClient(config["MONGO_URL"])
    app.db = client[config["ITEM"]]
    yield
    client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(authen.router)
app.include_router(item.router)




