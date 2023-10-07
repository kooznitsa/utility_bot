from typing import Optional

from sqlalchemy.orm import selectinload
from sqlmodel import select

from .base import BaseRepository
from schemas.articles import Article, ArticleCreate, ArticleRead
from schemas.tags import Tag
from schemas.districts import District


class ArticleRepository(BaseRepository):
    model = Article

    async def create(self, model_create: ArticleCreate) -> ArticleRead:
        model_query = select(self.model).where(self.model.url == model_create.url)
        result = await self._upsert(model_query, self.model, model_create)
        await self._add_to_db(result)
        return result

    async def list(
        self,
        limit: int = 50,
        tag: Optional[list[str]] = None,
        district: Optional[list[str]] = None,
        offset: int = 0,
    ) -> list[ArticleRead]:
        query = select(self.model).order_by(self.model.id)
        if tag:
            query = query.where(self.model.tags.any(Tag.tag.in_(tag)))
        if district:
            query = query.where(self.model.districts.any(District.district.in_(district)))
        query = query.offset(offset).limit(limit)
        results = await self.session.exec(query.options(selectinload('*')))
        return results.all()

    async def get(self, model_id: int) -> Optional[ArticleRead]:
        return await super().get(self.model, model_id)
