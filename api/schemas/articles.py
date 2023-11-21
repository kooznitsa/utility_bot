from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .link_schemas import ArticleDistrict
from .districts import DistrictRead
if TYPE_CHECKING:
    from .districts import District


class ArticleBase(SQLModel):
    url: str
    title: str
    content: str
    created_at: datetime
    pub_date: date = Field(index=True)
    deadline: date = Field(index=True)


class Article(ArticleBase, table=True):
    __tablename__ = 'articles'
    __table_args__ = (UniqueConstraint('url'),)

    id: int | None = Field(primary_key=True, default=None)

    districts: list['District'] = Relationship(back_populates='articles', link_model=ArticleDistrict)


class ArticleCreate(ArticleBase):
    pass


class ArticleRead(ArticleBase):
    id: int
    created_at: datetime
    districts: list[DistrictRead] = []
