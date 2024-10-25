from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Author
from schemas import AuthorCreate


async def create_author(author: AuthorCreate, db: AsyncSession) -> Author:
    new_author = Author(**author.model_dump())
    db.add(new_author)
    await db.commit()
    await db.refresh(new_author)
    return new_author


async def get_authors(db: AsyncSession) -> list[Author]:
    result = await db.execute(select(Author).order_by(Author.id))
    return result.scalars().all()


async def get_author(db: AsyncSession, author_id: int) -> Author | None:
    result = await db.execute(select(Author).where(Author.id == author_id))
    return result.scalar_one_or_none()


async def update_author(author_id: int, author_data: AuthorCreate, db: AsyncSession) -> Author:
    author = await get_author(db, author_id)
    if author:
        for k, v in author_data.model_dump().items():
            setattr(author, k, v)
        db.add(author)
        await db.commit()
        await db.refresh(author)
    return author


async def partial_update_author(author_id: int, author_data: AuthorCreate, db: AsyncSession) -> Author:
    author = await get_author(db, author_id)
    if author:
        for k, v in author_data.model_dump(exclude_unset=True).items():
            setattr(author, k, v)
        db.add(author)
        await db.commit()
        await db.refresh(author)
        return author


async def remove_author(author_id: int, db: AsyncSession) -> None:
    author = await get_author(db, author_id)
    if author:
        await db.delete(author)
        await db.commit()
        