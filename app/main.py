from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config import settings
from .session import create_db_and_tables
from .routers import cats, missions


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    description="API for Spy Cat Agency management",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(cats.router)
app.include_router(missions.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Spy Cat Agency API",
        "docs": "/docs",
        "redoc": "/redoc",
    }
