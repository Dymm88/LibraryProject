from pydantic import BaseModel, ConfigDict


class TagBaseSchema(BaseModel):
    name: str


class TagCreateSchema(TagBaseSchema):
    model_config = ConfigDict(from_attributes=True)
