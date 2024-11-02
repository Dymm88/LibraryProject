from asyncio import current_task

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://user:password@db:5432/library"
    db_echo: bool = True


class WorkerDB:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_session(self):
        return async_scoped_session(
            session_factory=self.session,
            scopefunc=current_task,
        )

    async def get_db(self):
        async with self.session() as session:
            yield session
            await session.close()


settings = Settings()

db_handler = WorkerDB(url=settings.db_url, echo=settings.db_echo)
