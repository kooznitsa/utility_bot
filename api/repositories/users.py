from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from .base import BaseRepository
from database.errors import EntityDoesNotExist, EntityAlreadyExists
from schemas.users import User, UserCreate, UserRead
from schemas.districts import District


class UserRepository(BaseRepository):
    model = User

    async def _get_user(self, model_id: int):
        query = select(self.model).where(self.model.user_id == model_id)
        result = await self.session.scalars(query.options(selectinload('*')))
        return result.first()

    async def create(self, model_create: UserCreate) -> UserRead:
        model_query = await self.session.execute(
            select(self.model)
            .where(self.model.user_id == model_create.user_id)
        )
        if not model_query.scalars().first():
            result = self.model.from_orm(model_create)
            await self._add_to_db(result)
            return result
        else:
            raise EntityAlreadyExists

    async def list_users(
        self,
        limit: int = 50,
        district: Optional[list[str]] = None,
        offset: int = 0,
    ) -> list[UserRead]:
        query = select(self.model).order_by(self.model.pub_date.desc())

        if district:
            query = query.where(self.model.districts.any(District.district.in_(district)))

        query = query.offset(offset).limit(limit)
        results = await self.session.execute(query.options(selectinload('*')))
        return results.scalars().all()

    async def get(self, model_id: int) -> Optional[UserRead]:
        if item := await self._get_user(model_id):
            return item
        else:
            raise EntityDoesNotExist

    async def delete_district(self, model_id: int, district_id: int) -> Optional[UserRead]:
        district_to_delete = await self._get_instance(District, district_id)
        instance = await self._get_user(model_id)

        if instance and (district_to_delete in instance.districts):
            instance.districts.remove(district_to_delete)
            await self._add_to_db(instance)
            return instance
        else:
            raise EntityDoesNotExist
