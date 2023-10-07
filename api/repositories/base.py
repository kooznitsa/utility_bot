from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from database.errors import EntityDoesNotExist


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_instance(self, model, model_id: int):
        query = select(model).where(model.id == model_id)
        result = await self.session.scalars(query.options(selectinload('*')))
        return result.first()

    async def get_list(self, query):
        results = await self.session.exec(query.options(selectinload('*')))
        # return results.all()
        try:
            return results.scalars().all()
        except AttributeError:
            return results.all()

    async def _add_to_db(self, new_item):
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)

    async def _upsert(self, query, model, model_create):
        result = await self.session.execute(query)
        # result = result.scalars().first()
        try:
            result = result.first()[0]
        except AttributeError:
            result = result.scalars().first()
        model_from_orm = model.from_orm(model_create)

        if result is None:
            result = model_from_orm

        for k, v in model_from_orm.dict(exclude_unset=True).items():
            setattr(result, k, v)

        return result

    async def list(self, model, limit: int = 50, offset: int = 0):
        query = select(model).order_by(model.id).offset(offset).limit(limit)
        return await self.get_list(query)

    async def get(self, model, model_id: int):
        if item := await self._get_instance(model, model_id):
            return item
        else:
            raise EntityDoesNotExist

    async def delete(self, model, model_id: int) -> None:
        if item := await self._get_instance(model, model_id):
            await self.session.delete(item)
            await self.session.commit()
        else:
            raise EntityDoesNotExist
