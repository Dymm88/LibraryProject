from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import BookBase, BookCreate
from service import BookCRUD

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookBase, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    book_crud = BookCRUD(session=db)
    return await book_crud.create_book(book=book)


@router.get("/", response_model=list[BookBase])
async def get_books(db: AsyncSession = Depends(db_handler.get_db)):
    book_crud = BookCRUD(session=db)
    result = await book_crud.get_books()
    return [BookBase(title=c.title, created_at=c.created_at, genre=c.genre, author_id=c.author_id) for c in result]


@router.get("/{book_id}", response_model=BookBase)
async def get_book(book_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    book_crud = BookCRUD(session=db)
    book = await book_crud.get_book(book_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{book_id}", response_model=BookBase, status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_id: int, book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    book_crud = BookCRUD(session=db)
    mod_book = await book_crud.update_book(book_id=book_id, book_data=book)
    return mod_book


@router.patch("/{book_id}", response_model=BookBase, status_code=status.HTTP_202_ACCEPTED)
async def partial_update_book(book_id: int, book: BookCreate, db: AsyncSession = Depends(db_handler.get_db)):
    book_crud = BookCRUD(session=db)
    mod_book = await book_crud.partial_update_book(book_id=book_id, book_data=book)
    return mod_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(book_id: int, db: AsyncSession = Depends(db_handler.get_db)) -> None:
    book_crud = BookCRUD(session=db)
    await book_crud.remove_book(book_id=book_id)
