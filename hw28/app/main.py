from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routers import items


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="FastAPI CRUD Demo", lifespan=lifespan)

app.include_router(items.router, prefix="/items", tags=["items"])


@app.get("/")
async def root():
    return {"message": "Hello, FastAPI CRUD"}
