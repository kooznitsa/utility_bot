from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.errors import EntityDoesNotExist
from repositories.base import BaseRepository
from schemas.districts import District, DistrictCreate, DistrictRead


class DistrictRepository(BaseRepository):
    model = District

    async def create(self, model_id: int, district_create: DistrictCreate, parent_model) -> DistrictRead:
        model_query = await self.session.scalars(
            select(parent_model)
            .where(parent_model.id == model_id)
            .options(selectinload(parent_model.districts))
        )
        if item := model_query.first():
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
