from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .link_schemas import ArticleDistrict
if TYPE_CHECKING:
    from .articles import Article


class DistrictBase(SQLModel):
    district: str


class District(DistrictBase, table=True):
    __tablename__ = 'districts'
    __table_args__ = (UniqueConstraint('district'),)

    id: int | None = Field(primary_key=True, default=None)

    articles: list['Article'] = Relationship(back_populates='districts', link_model=ArticleDistrict)


class DistrictCreate(DistrictBase):
    pass


class DistrictRead(DistrictBase):
    id: int
