from src.schemas.comforts import ComfortAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class ComfortService(BaseService):
    async def create_comfort(self, data: ComfortAdd):
        comfort = await self.db.comforts.add(data)
        await self.db.commit()
        test_task.delay()  # type: ignore
        return comfort

    async def get_all_comforts(self):
        return await self.db.comforts.get_all()
