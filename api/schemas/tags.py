from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .link_schemas import ArticleTag
if TYPE_CHECKING:
    from .articles import Article


class TagBase(SQLModel):
    tag: str


class Tag(TagBase, table=True):
    __tablename__ = 'tags'
    __table_args__ = (UniqueConstraint('tag'),)

    id: int | None = Field(primary_key=True, default=None)

    articles: list['Article'] = Relationship(back_populates='tags', link_model=ArticleTag)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int
