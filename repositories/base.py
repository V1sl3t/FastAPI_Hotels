from dns.e164 import query
from sqlalchemy import select, insert

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_one()

    async def add(self, kwargs):
        add_stmt = insert(self.model).values(**kwargs.model_dump()).returning()
        print(add_stmt.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_stmt)
        return result
