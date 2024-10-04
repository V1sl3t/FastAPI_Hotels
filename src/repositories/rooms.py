from pydantic import BaseModel
from sqlalchemy import select, func, insert

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self,
            hotel_id,
            title,
            price

    ) -> list[Room]:
        query = select(RoomsOrm).filter_by(hotel_id=hotel_id)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.rstrip().lower()))
        if price:
            query = query.filter_by(price=price)
        result = await self.session.execute(query)
        return [self.schema.model_validate(room, from_attributes=True) for room in result.scalars().all()]
