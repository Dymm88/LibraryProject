from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import BookBase, BookCreate
from service import book as crud

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookBase)
async def create_book(book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    return await crud.create_book(book=book, db=db)


@router.get("/", response_model=list[BookBase])
async def get_books(db: AsyncSession = Depends(db_handler.get_db)):
    result = await crud.get_books(db=db)
    return [BookBase(title=c.title, created_at=c.created_at, genre=c.genre, author_id=c.author_id) for c in result]


@router.get("/{book_id}", response_model=BookBase)
async def get_book(book_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    book = await crud.get_book(db=db, book_id=book_id)
    return book


@router.put("/{book_id}", response_model=BookBase)
async def update_book(book_id: int, book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    mod_book = await crud.update_book(db=db, book_id=book_id, book_data=book)
    return mod_book


@router.patch("/{book_id}", response_model=BookBase)
async def partial_update_book(book_id: int, book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    mod_book = await crud.partial_update_book(db=db, book_id=book_id, book_data=book)
    return mod_book


@router.delete("/{author_id}")
async def remove_book(book_id: int, db: AsyncSession = Depends(db_handler.get_db)) -> None:
    await crud.remove_book(book_id=book_id, db=db)
