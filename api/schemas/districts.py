from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .link_schemas import ArticleDistrict, UserDistrict
if TYPE_CHECKING:
    from .articles import Article
    from .users import User


class DistrictBase(SQLModel):
    district: str


class District(DistrictBase, table=True):
    __tablename__ = 'districts'
    __table_args__ = (UniqueConstraint('district'),)

    id: int | None = Field(primary_key=True, default=None)

    articles: list['Article'] = Relationship(back_populates='districts', link_model=ArticleDistrict)
    users: list['User'] = Relationship(back_populates='districts', link_model=UserDistrict)


class DistrictCreate(DistrictBase):
    pass


class DistrictRead(DistrictBase):
    id: int
