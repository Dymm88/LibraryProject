from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    name: str
    country: str


class AuthorCreateSchema(AuthorBaseSchema):
    model_config = ConfigDict(from_attributes=True)
