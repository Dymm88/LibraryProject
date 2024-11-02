from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import TagBaseSchema, TagCreateSchema
from service import TagCRUD

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagBaseSchema, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: TagCreateSchema, session: AsyncSession = Depends(db_handler.get_db)
):
    return await TagCRUD(session=session).create(tag=tag)


@router.get("/", response_model=list[TagBaseSchema])
async def get_tags(session: AsyncSession = Depends(db_handler.get_db)):
    result = await TagCRUD(session=session).get_all()
    return [TagBaseSchema(name=tag_data.name) for tag_data in result]


@router.get("/{tag_id}", response_model=TagBaseSchema)
async def get_tag(tag_id: int, session: AsyncSession = Depends(db_handler.get_db)):
    tag = await TagCRUD(session=session).get_one(tag_id=tag_id)
    if tag:
        return tag
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put(
    "/{tag_id}", response_model=TagBaseSchema, status_code=status.HTTP_202_ACCEPTED
)
async def update_tag(
    tag_id: int,
    tag: TagCreateSchema,
    session: AsyncSession = Depends(db_handler.get_db),
):
    mod_tag = await TagCRUD(session=session).update(tag_id=tag_id, tag_data=tag)
    return mod_tag


@router.patch(
    "/{tag_id}", response_model=TagBaseSchema, status_code=status.HTTP_202_ACCEPTED
)
async def partial_update_tag(
    tag_id: int,
    tag: TagCreateSchema,
    session: AsyncSession = Depends(db_handler.get_db),
):
    mod_tag = await TagCRUD(session=session).partial_update(tag_id=tag_id, tag_data=tag)
    return mod_tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag(
    tag_id: int, session: AsyncSession = Depends(db_handler.get_db)
) -> None:
    await TagCRUD(session=session).remove(tag_id=tag_id)
