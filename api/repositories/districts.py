from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.errors import EntityDoesNotExist
from schemas.articles import Article
from schemas.districts import District, DistrictCreate, DistrictRead
from repositories.base import BaseRepository


class DistrictRepository(BaseRepository):
    model = District

    async def create(self, model_id: int, district_create: DistrictCreate) -> DistrictRead:
        model_query = await self.session.execute(
            select(Article)
            .where(Article.id == model_id)
            .options(selectinload(Article.districts))
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

    async def get(self, model_id: int) -> Optional[DistrictRead]:
        return await super().get(self.model, model_id)
