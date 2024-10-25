from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import AuthorCreate, AuthorBase
from service import author as crud

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorBase)
async def create_author(author: AuthorCreate, db: AsyncSession = Depends(db_handler.get_db)):
    return await crud.create_author(author=author, db=db)


@router.get("/", response_model=list[AuthorBase])
async def get_authors(db: AsyncSession = Depends(db_handler.get_db)):
    result = await crud.get_authors(db=db)
    return [AuthorBase(name=c.name, country=c.country) for c in result]


@router.get("/{author_id}", response_model=AuthorBase)
async def get_author(author_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    author = await crud.get_author(db=db, author_id=author_id)
    return author


@router.put("/{author_id}", response_model=AuthorBase)
async def update_author(author_id: int, author: AuthorCreate, db: AsyncSession = Depends(db_handler.get_db)):
    mod_author = await crud.update_author(db=db, author_id=author_id, author_data=author)
    return mod_author


@router.patch("/{author_id}", response_model=AuthorBase)
async def partial_update_author(author_id: int, author: AuthorCreate, db: AsyncSession = Depends(db_handler.get_db)):
    mod_author = await crud.partial_update_author(db=db, author_id=author_id, author_data=author)
    return mod_author


@router.delete("/{author_id}")
async def remove_author(author_id: int, db: AsyncSession = Depends(db_handler.get_db)) -> None:
    await crud.remove_author(author_id=author_id, db=db)
