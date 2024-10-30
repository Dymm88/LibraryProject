from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import AuthorCreate, AuthorBase
from service import AuthorCRUD

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorBase, status_code=status.HTTP_201_CREATED)
async def create_author(new_author: AuthorCreate, session: AsyncSession = Depends(db_handler.get_db)):
    author_crud = AuthorCRUD(session)
    return await author_crud.create_author(author=new_author)


@router.get("/", response_model=list[AuthorBase])
async def get_authors(session: AsyncSession = Depends(db_handler.get_db)):
    author_crud = AuthorCRUD(session)
    result = await author_crud.get_authors()
    return [AuthorBase(name=author_data.name, country=author_data.country) for author_data in result]


@router.get("/{author_id}", response_model=AuthorBase)
async def get_author(author_id: int, session: AsyncSession = Depends(db_handler.get_db)):
    author_crud = AuthorCRUD(session)
    one_author = await author_crud.get_author(author_id=author_id)
    if one_author:
        return one_author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{author_id}", response_model=AuthorBase, status_code=status.HTTP_202_ACCEPTED)
async def update_author(author_id: int, replace_author: AuthorCreate,
                        session: AsyncSession = Depends(db_handler.get_db)):
    author_crud = AuthorCRUD(session)
    mod_author = await author_crud.update_author(author_id=author_id, author_data=replace_author)
    return mod_author


@router.patch("/{author_id}", response_model=AuthorBase, status_code=status.HTTP_202_ACCEPTED)
async def partial_update_author(author_id: int, replace_author: AuthorCreate,
                                session: AsyncSession = Depends(db_handler.get_db)):
    author_crud = AuthorCRUD(session)
    mod_author = await author_crud.partial_update_author(author_id=author_id, author_data=replace_author)
    return mod_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_author(author_id: int, session: AsyncSession = Depends(db_handler.get_db)) -> None:
    author_crud = AuthorCRUD(session)
    await author_crud.remove_author(author_id=author_id)
