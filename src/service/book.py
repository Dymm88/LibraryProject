from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Book
from schemas import BookCreate


async def create_book(book: BookCreate, db: AsyncSession) -> Book:
    new_book = Book(**book.model_dump())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book


async def get_books(db: AsyncSession) -> list[Book]:
    result = await db.execute(select(Book).order_by(Book.id))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int) -> Book | None:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(book_id: int, book_data: BookCreate, db: AsyncSession) -> Book:
    book = await get_book(db, book_id)
    if book:
        for k, v in book_data.model_dump().items():
            setattr(book, k, v)
        db.add(book)
        await db.commit()
        await db.refresh(book)
    return book


async def partial_update_book(book_id: int, book_data: BookCreate, db: AsyncSession) -> Book:
    book = await get_book(db, book_id)
    if book:
        for k, v in book_data.model_dump(exclude_unset=True).items():
            setattr(book, k, v)
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book


async def remove_book(book_id: int, db: AsyncSession) -> None:
    book = await get_book(db, book_id)
    if book:
        await db.delete(book)
        await db.commit()
