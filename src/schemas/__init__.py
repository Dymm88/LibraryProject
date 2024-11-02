__all__ = (
    "AuthorBaseSchema",
    "AuthorCreateSchema",
    "BookBaseSchema",
    "BookCreateSchema",
    "TagBaseSchema",
    "TagCreateSchema",
)

from .author import AuthorBaseSchema, AuthorCreateSchema
from .book import BookBaseSchema, BookCreateSchema
from .tag import TagBaseSchema, TagCreateSchema
