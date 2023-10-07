from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.errors import EntityDoesNotExist
from repositories.base import BaseRepository
from schemas.tags import Tag, TagCreate, TagRead
from schemas.articles import Article


class TagRepository(BaseRepository):
    model = Tag

    async def create(self, model_id: int, tag_create: TagCreate) -> TagRead:
        model_query = await self.session.scalars(
            select(Article)
            .where(Article.id == model_id)
            .options(selectinload('*'))
        )

        if item := model_query.first():
            tag_query = select(self.model).where(self.model.tag == tag_create.tag)
            new_tag = await self._upsert(tag_query, Tag, tag_create)
            self.session.add(new_tag)
            item.tags.append(new_tag)
            await self.session.commit()
            await self.session.refresh(new_tag)
            return new_tag
        else:
            raise EntityDoesNotExist

    async def get(self, model_id: int) -> Optional[TagRead]:
        return await super().get(self.model, model_id)
