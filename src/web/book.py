from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import BookBase, BookCreate
from service import BookCRUD

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookBase, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, session: AsyncSession = Depends(db_handler.get_db)):
    return await BookCRUD(session=session).create_book(book=book)


@router.get("/", response_model=list[BookBase])
async def get_books(session: AsyncSession = Depends(db_handler.get_db)):
    result = await BookCRUD(session=session).get_books()
    return [BookBase(title=book_data.title, created_at=book_data.created_at, genre=book_data.genre,
                     author_id=book_data.author_id) for book_data in result]


@router.get("/{book_id}", response_model=BookBase)
async def get_book(book_id: int, session: AsyncSession = Depends(db_handler.get_db)):
    book = await BookCRUD(session=session).get_book(book_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{book_id}", response_model=BookBase, status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_id: int, book: BookCreate, session: AsyncSession = Depends(db_handler.get_db)):
    mod_book = await BookCRUD(session=session).update_book(book_id=book_id, book_data=book)
    return mod_book


@router.patch("/{book_id}", response_model=BookBase, status_code=status.HTTP_202_ACCEPTED)
async def partial_update_book(book_id: int, book: BookCreate, session: AsyncSession = Depends(db_handler.get_db)):
    mod_book = await BookCRUD(session=session).partial_update_book(book_id=book_id, book_data=book)
    return mod_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(book_id: int, session: AsyncSession = Depends(db_handler.get_db)) -> None:
    await BookCRUD(session=session).remove_book(book_id=book_id)
