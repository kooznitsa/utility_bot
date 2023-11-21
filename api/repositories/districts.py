from typing import TYPE_CHECKING, Union

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.errors import EntityDoesNotExist
from schemas.districts import District, DistrictCreate, DistrictRead
from repositories.base import BaseRepository

if TYPE_CHECKING:
    from schemas.articles import Article
    from schemas.users import User


class DistrictRepository(BaseRepository):
    model = District

    async def create(
            self,
            model_id: int,
            district_create: DistrictCreate,
            parent_model: Union['Article', 'User'],
    ) -> DistrictRead:
        if parent_model.__name__ == 'Article':
            model_query = await self.session.execute(
                select(parent_model)
                .where(parent_model.id == model_id)
                .options(selectinload(parent_model.districts))
            )
        elif parent_model.__name__ == 'User':
            model_query = await self.session.execute(
                select(parent_model)
                .where(parent_model.user_id == model_id)
                .options(selectinload(parent_model.districts))
            )
        if item := model_query.scalars().first():
            district_query = select(self.model).where(self.model.district == district_create.district)
            new_district = await self._upsert(district_query, District, district_create)
            self.session.add(new_district)
            item.districts.append(new_district)
            await self.session.commit()
            await self.session.refresh(new_district)
            return new_district
        else:
            raise EntityDoesNotExist
