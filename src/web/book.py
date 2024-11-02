from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import BookBaseSchema, BookCreateSchema
from service import BookCRUD

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookBaseSchema, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: BookCreateSchema, session: AsyncSession = Depends(db_handler.get_db)
):
    return await BookCRUD(session=session).create(book=book)


@router.get("/", response_model=list[BookBaseSchema])
async def get_books(session: AsyncSession = Depends(db_handler.get_db)):
    result = await BookCRUD(session=session).get_all()
    return [
        BookBaseSchema(
            title=book_data.title,
            created_at=book_data.created_at,
            genre=book_data.genre,
            author_id=book_data.author_id,
        )
        for book_data in result
    ]


@router.get("/{book_id}", response_model=BookBaseSchema)
async def get_book(book_id: int, session: AsyncSession = Depends(db_handler.get_db)):
    book = await BookCRUD(session=session).get_one(book_id=book_id)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put(
    "/{book_id}", response_model=BookBaseSchema, status_code=status.HTTP_202_ACCEPTED
)
async def update_book(
    book_id: int,
    book: BookCreateSchema,
    session: AsyncSession = Depends(db_handler.get_db),
):
    mod_book = await BookCRUD(session=session).update(book_id=book_id, book_data=book)
    return mod_book


@router.patch(
    "/{book_id}", response_model=BookBaseSchema, status_code=status.HTTP_202_ACCEPTED
)
async def partial_update_book(
    book_id: int,
    book: BookCreateSchema,
    session: AsyncSession = Depends(db_handler.get_db),
):
    mod_book = await BookCRUD(session=session).partial(book_id=book_id, book_data=book)
    return mod_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_book(
    book_id: int, session: AsyncSession = Depends(db_handler.get_db)
) -> None:
    await BookCRUD(session=session).remove(book_id=book_id)
