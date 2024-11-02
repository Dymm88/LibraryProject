from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Author
from schemas import AuthorCreate


class AuthorCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, author: AuthorCreate) -> Author:
        new_author = Author(**author.model_dump())
        self.session.add(new_author)
        await self.session.commit()
        await self.session.refresh(new_author)
        return new_author
    
    async def get_all(self) -> list[Author]:
        result = await self.session.execute(select(Author).order_by(Author.id))
        return result.scalars().all()
    
    async def get_one(self, author_id: int) -> Author | None:
        result = await self.session.execute(select(Author).where(Author.id == author_id))
        return result.scalar_one_or_none()
    
    async def update(self, author_id: int, author_data: AuthorCreate) -> Author:
        author = await self.get_one(author_id)
        if author:
            for k, v in author_data.model_dump().items():
                setattr(author, k, v)
            self.session.add(author)
            await self.session.commit()
            await self.session.refresh(author)
        return author
    
    async def partial_update(self, author_id: int, author_data: AuthorCreate) -> Author:
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
