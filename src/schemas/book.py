from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    created_at: int
    genre: str
    author_id: int


class BookCreate(BookBase):
    model_config = ConfigDict(from_attributes=True)
