from contextlib import asynccontextmanager

from fastapi import FastAPI

from data import db_handler
from models import Base
from web import author, book, tag


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_handler.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Library", lifespan=lifespan)

app.include_router(author.router)
app.include_router(book.router)
app.include_router(tag.router)
