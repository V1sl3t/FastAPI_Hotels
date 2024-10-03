from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ) -> list[Hotel]:
        query = select(HotelsOrm)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.rstrip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.rstrip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
