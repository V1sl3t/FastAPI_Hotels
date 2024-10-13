from datetime import date

from pydantic import BaseModel
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import selectinload

from src.exceptions import ObjectNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.comforts))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none_with_rels(self, **filter_by):
        try:
            query = select(self.model).options(selectinload(self.model.comforts)).filter_by(**filter_by)
            result = await self.session.execute(query)
            model = result.scalars().one_or_none()
            return RoomDataWithRelsMapper.map_to_domain_entity(model)
        except NoResultFound:
            raise ObjectNotFoundException

    async def add(self, data: BaseModel):
        try:
            add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
        except IntegrityError:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(edit_stmt)

