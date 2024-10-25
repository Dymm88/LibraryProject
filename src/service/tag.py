from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Tag
from schemas import TagCreate


async def create_tag(tag: TagCreate, db: AsyncSession) -> Tag:
    new_tag = Tag(**tag.model_dump())
    db.add(new_tag)
    await db.commit()
    await db.refresh(new_tag)
    return new_tag


async def get_tags(db: AsyncSession) -> list[Tag]:
    result = await db.execute(select(Tag).order_by(Tag.id))
    return result.scalars().all()


async def get_tag(db: AsyncSession, tag_id: int) -> Tag | None:
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    return result.scalar_one_or_none()


async def update_tag(tag_id: int, tag_data: TagCreate, db: AsyncSession) -> Tag:
    tag = await get_tag(db, tag_id)
    if tag:
        for k, v in tag_data.model_dump().items():
            setattr(tag, k, v)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
    return tag


async def partial_update_tag(tag_id: int, tag_data: TagCreate, db: AsyncSession) -> Tag:
    tag = await get_tag(db, tag_id)
    if tag:
        for k, v in tag_data.model_dump(exclude_unset=True).items():
            setattr(tag, k, v)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        return tag


async def remove_tag(tag_id: int, db: AsyncSession) -> None:
    tag = await get_tag(db, tag_id)
    if tag:
        await db.delete(tag)
        await db.commit()
