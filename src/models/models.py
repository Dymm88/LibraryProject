from sqlalchemy import Integer, ForeignKey, String, Table, Column
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)


author_tags = Table(
    'author_tags',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

book_tags = Table(
    'book_tags',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Author(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    books = relationship("Book", back_populates="author")
    tags = relationship("Tag", secondary=author_tags, back_populates="authors")


class Book(Base):
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")
    tags = relationship("Tag", secondary=book_tags, back_populates="books")


class Tag(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    books = relationship("Book", secondary=book_tags, back_populates="tags")
    authors = relationship("Author", secondary=author_tags, back_populates="tags")
