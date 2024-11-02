from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book
from schemas import BookCreate

class BookCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, book: BookCreate) -> Book:
        new_book = Book(**book.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        await self.session.refresh(new_book)
        return new_book

    async def get_all(self) -> list[Book]:
        result = await self.session.execute(select(Book).order_by(Book.id))
        return result.scalars().all()

    async def get_one(self, book_id: int) -> Book | None:
        result = await self.session.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    async def update(self, book_id: int, book_data: BookCreate) -> Book:
        book = await self.get_one(book_id)
        if book:
            for k, v in book_data.model_dump().items():
                setattr(book, k, v)
            self.session.add(book)
            await self.session.commit()
            await self.session.refresh(book)
        return book

    async def partial(self, book_id: int, book_data: BookCreate) -> Book:
        book = await self.get_one(book_id)
        if book:
            for k, v in book_data.model_dump(exclude_unset=True).items():
                setattr(book, k, v)
            self.session.add(book)
            await self.session.commit()
            await self.session.refresh(book)
            return book

    async def remove(self, book_id: int) -> None:
        book = await self.get_one(book_id)
        if book:
            await self.session.delete(book)
            await self.session.commit()
