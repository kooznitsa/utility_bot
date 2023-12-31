from datetime import date
from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from .base import BaseRepository
from schemas.articles import Article, ArticleCreate, ArticleRead
from schemas.districts import District
from utils.async_iterator import AsyncItemIterator


class ArticleRepository(BaseRepository):
    model = Article

    async def create(self, model_create: ArticleCreate) -> ArticleRead:
        model_query = await self.session.execute(
            select(self.model)
            .where(self.model.url == model_create.url)
        )
        if not model_query.scalars().first() and model_create.deadline >= date.today():
            result = self.model.from_orm(model_create)
            await self._add_to_db(result)
            return result
        return

    async def list(
        self,
        limit: int = 50,
        district: Optional[list[str]] = None,
        offset: int = 0,
    ) -> list[ArticleRead]:
        query = select(self.model).order_by(self.model.pub_date.desc())
        today = date.today()

        if district:
            query = query.where(self.model.districts.any(District.district.in_(district)))

        query = query.where(self.model.deadline >= today).offset(offset).limit(limit)
        results = await self.session.execute(query.options(selectinload('*')))
        return results.scalars().all()

    async def get(self, model_id: int) -> Optional[ArticleRead]:
        return await super().get(self.model, model_id)

    async def delete_bunch(self):
        query = select(self.model).where(self.model.deadline < date.today())
        articles_to_delete = await self.session.execute(query.options(selectinload('*')))
        async for article in AsyncItemIterator(articles_to_delete.scalars().all()):
            await self.session.delete(article)
        await self.session.commit()
