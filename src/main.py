from contextlib import asynccontextmanager

from fastapi import FastAPI

import models
from data import db_handler
from web.author import router as author_router
from web.book import router as book_router
from web.tag import router as tag_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_handler.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        yield


app = FastAPI(title="Library", lifespan=lifespan)

app.include_router(author_router)
app.include_router(book_router)
app.include_router(tag_router)
