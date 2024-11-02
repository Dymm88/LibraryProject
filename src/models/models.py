from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class AuthorTag(Base):
    __tablename__ = "author_tags"

    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("authors.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tags.id"), primary_key=True
    )

    author: Mapped["AuthorModel"] = relationship(
        "AuthorModel", back_populates="author_tags"
    )
    tag: Mapped["TagModel"] = relationship("TagModel", back_populates="author_tags")


class BookTag(Base):
    __tablename__ = "book_tags"

    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id"), primary_key=True
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tags.id"), primary_key=True
    )

    book: Mapped["BookModel"] = relationship("BookModel", back_populates="book_tags")
    tag: Mapped["TagModel"] = relationship("TagModel", back_populates="book_tags")


class AuthorModel(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)

    books: Mapped[list["BookModel"]] = relationship(
        "BookModel", back_populates="author"
    )
    author_tags: Mapped[list[AuthorTag]] = relationship(
        "AuthorTag", back_populates="author"
    )


class BookModel(Base):
    title: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String, nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("authors.id"))
    author: Mapped["AuthorModel"] = relationship("AuthorModel", back_populates="books")
    book_tags: Mapped[list[BookTag]] = relationship("BookTag", back_populates="book")


class TagModel(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)

    author_tags: Mapped[list[AuthorTag]] = relationship(
        "AuthorTag", back_populates="tag"
    )
    book_tags: Mapped[list[BookTag]] = relationship("BookTag", back_populates="tag")
