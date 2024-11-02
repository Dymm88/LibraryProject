from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import AuthorCreateSchema, AuthorBaseSchema
from service import AuthorCRUD

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorBaseSchema, status_code=status.HTTP_201_CREATED)
async def create_author(
    new_author: AuthorCreateSchema, session: AsyncSession = Depends(db_handler.get_db)
):
    return await AuthorCRUD(session).create(author=new_author)


@router.get("/", response_model=list[AuthorBaseSchema])
async def get_authors(session: AsyncSession = Depends(db_handler.get_db)):
    result = await AuthorCRUD(session).get_all()
    return [
        AuthorBaseSchema(name=author_data.name, country=author_data.country)
        for author_data in result
    ]


@router.get("/{author_id}", response_model=AuthorBaseSchema)
async def get_author(
    author_id: int, session: AsyncSession = Depends(db_handler.get_db)
):
    one_author = await AuthorCRUD(session).get_one(author_id=author_id)
    if one_author:
        return one_author
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put(
    "/{author_id}",
    response_model=AuthorBaseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_author(
    author_id: int,
    replace_author: AuthorCreateSchema,
    session: AsyncSession = Depends(db_handler.get_db),
):
    mod_author = await AuthorCRUD(session).update(
        author_id=author_id, author_data=replace_author
    )
    return mod_author


@router.patch(
    "/{author_id}",
    response_model=AuthorBaseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def partial_update_author(
    author_id: int,
    replace_author: AuthorCreateSchema,
    session: AsyncSession = Depends(db_handler.get_db),
):
    mod_author = await AuthorCRUD(session).partial_update(
        author_id=author_id, author_data=replace_author
    )
    return mod_author


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_author(
    author_id: int, session: AsyncSession = Depends(db_handler.get_db)
) -> None:
    await AuthorCRUD(session).remove(author_id=author_id)
