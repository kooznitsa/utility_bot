from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from .base import BaseRepository
from database.errors import EntityDoesNotExist, EntityAlreadyExists
from schemas.users import User, UserCreate, UserRead
from schemas.districts import District
from schemas.articles import Article, ArticleRead


class UserRepository(BaseRepository):
    model = User

    async def _get_user(self, model_id: int):
        query = select(self.model).where(self.model.user_id == model_id)
        result = await self.session.execute(query.options(selectinload('*')))
        return result.scalars().first()

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
        query = select(self.model)

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

    async def delete_all_districts(self, model_id: int) -> Optional[UserRead]:
        if instance := await self._get_user(model_id):
            instance.districts.clear()
            await self._add_to_db(instance)
            return await self._get_user(model_id)
        else:
            raise EntityDoesNotExist

    async def list_articles(self, model_id: int) -> list[ArticleRead]:
        if instance := await self._get_user(model_id):
            districts = [i.district for i in instance.districts]
            articles_query = (
                select(Article)
                .where(Article.districts.any(District.district.in_(districts)))
                .where(Article.created_at >= (datetime.now() - timedelta(minutes=30)))
                .distinct()
                .order_by(Article.created_at)
            )

            results = await self.session.execute(articles_query.options(selectinload('*')))
            return results.scalars().all()

        else:
            raise EntityDoesNotExist
