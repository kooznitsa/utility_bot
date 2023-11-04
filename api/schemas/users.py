from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .districts import DistrictRead
from .link_schemas import UserDistrict
if TYPE_CHECKING:
    from .districts import District


class UserBase(SQLModel):
    user_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class User(UserBase, table=True):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('user_id'),)

    id: int | None = Field(primary_key=True, default=None)

    districts: list['District'] = Relationship(back_populates='users', link_model=UserDistrict)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    districts: list[DistrictRead] = []
