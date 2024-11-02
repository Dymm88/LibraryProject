from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import AuthorModel
from schemas import AuthorCreateSchema


class AuthorCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, author: AuthorCreateSchema) -> AuthorModel:
        new_author = AuthorModel(**author.model_dump())
        self.session.add(new_author)
        await self.session.commit()
        await self.session.refresh(new_author)
        return new_author

    async def get_all(self) -> list[AuthorModel]:
        result = await self.session.execute(
            select(AuthorModel).order_by(AuthorModel.id)
        )
        return result.scalars().all()

    async def get_one(self, author_id: int) -> AuthorModel | None:
        result = await self.session.execute(
            select(AuthorModel).where(AuthorModel.id == author_id)
        )
        return result.scalar_one_or_none()

    async def update(
        self, author_id: int, author_data: AuthorCreateSchema
    ) -> AuthorModel:
        author = await self.get_one(author_id)
        if author:
            for k, v in author_data.model_dump().items():
                setattr(author, k, v)
            self.session.add(author)
            await self.session.commit()
            await self.session.refresh(author)
        return author

    async def partial_update(
        self, author_id: int, author_data: AuthorCreateSchema
    ) -> AuthorModel:
        author = await self.get_one(author_id)
        if author:
            for k, v in author_data.model_dump(exclude_unset=True).items():
                setattr(author, k, v)
            self.session.add(author)
            await self.session.commit()
            await self.session.refresh(author)
            return author

    async def remove(self, author_id: int) -> None:
        author = await self.get_one(author_id)
        if author:
            await self.session.delete(author)
            await self.session.commit()
