from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            limit: int,
            offset: int
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
            .limit(limit)
            .offset(offset)
        )
        if location:
            hotels_ids_to_get = hotels_ids_to_get.filter(func.lower(HotelsOrm.location).contains(location.rstrip().lower()))
        if title:
            hotels_ids_to_get = hotels_ids_to_get.filter(func.lower(HotelsOrm.title).contains(title.rstrip().lower()))
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))