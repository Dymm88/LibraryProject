from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from schemas import TagBase, TagCreate
from service import tag as crud

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/", response_model=TagBase, status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagCreate, db: AsyncSession = Depends(db_handler.get_db)):
    return await crud.create_tag(tag=tag, db=db)


@router.get("/", response_model=list[TagBase])
async def get_tags(db: AsyncSession = Depends(db_handler.get_db)):
    result = await crud.get_tags(db=db)
    return [TagBase(name=c.name) for c in result]


@router.get("/{tag_id}", response_model=TagBase)
async def get_tag(tag_id: int, db: AsyncSession = Depends(db_handler.get_db)):
    tag = await crud.get_tag(db=db, tag_id=tag_id)
    if tag:
        return tag
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{tag_id}", response_model=TagBase, status_code=status.HTTP_202_ACCEPTED)
async def update_tag(tag_id: int, tag: TagCreate, db: AsyncSession = Depends(db_handler.get_db)):
    mod_tag = await crud.update_tag(db=db, tag_id=tag_id, tag_data=tag)
    return mod_tag


@router.patch("/{tag_id}", response_model=TagBase, status_code=status.HTTP_202_ACCEPTED)
async def partial_update_tag(tag_id: int, tag: TagCreate, db: AsyncSession = Depends(db_handler.get_db)):
    mod_tag = await crud.partial_update_tag(db=db, tag_id=tag_id, tag_data=tag)
    return mod_tag


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_tag(tag_id: int, db: AsyncSession = Depends(db_handler.get_db)) -> None:
    await crud.remove_tag(tag_id=tag_id, db=db)
