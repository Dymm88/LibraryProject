from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import TagModel
from schemas import TagCreateSchema


class TagCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tag: TagCreateSchema) -> TagModel:
        new_tag = TagModel(**tag.model_dump())
        self.session.add(new_tag)
        await self.session.commit()
        await self.session.refresh(new_tag)
        return new_tag

    async def get_all(self) -> list[TagModel]:
        result = await self.session.execute(select(TagModel).order_by(TagModel.id))
        return result.scalars().all()

    async def get_one(self, tag_id: int) -> TagModel | None:
        result = await self.session.execute(
            select(TagModel).where(TagModel.id == tag_id)
        )
        return result.scalar_one_or_none()

    async def update(self, tag_id: int, tag_data: TagCreateSchema) -> TagModel:
        tag = await self.get_one(tag_id)
        if tag:
            for k, v in tag_data.model_dump().items():
                setattr(tag, k, v)
            self.session.add(tag)
            await self.session.commit()
            await self.session.refresh(tag)
        return tag

    async def partial_update(self, tag_id: int, tag_data: TagCreateSchema) -> TagModel:
        tag = await self.get_one(tag_id)
        if tag:
            for k, v in tag_data.model_dump(exclude_unset=True).items():
                setattr(tag, k, v)
            self.session.add(tag)
            await self.session.commit()
            await self.session.refresh(tag)
            return tag

    async def remove(self, tag_id: int) -> None:
        tag = await self.get_one(tag_id)
        if tag:
            await self.session.delete(tag)
            await self.session.commit()
