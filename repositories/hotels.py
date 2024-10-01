from sqlalchemy import select, func, insert

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
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
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, hotel_data):
        add_hotel_stmt = insert(self.model).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_hotel_stmt)