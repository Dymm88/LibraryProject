from pydantic import BaseModel, ConfigDict


class AuthorBase(BaseModel):
    name: str
    country: str
    
    
class AuthorCreate(AuthorBase):
    model_config = ConfigDict(from_attributes=True)