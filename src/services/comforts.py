from src.schemas.comforts import ComfortAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def create_facility(self, data: ComfortAdd):
        comfort = await self.db.comforts.add(data)
        await self.db.commit()
        test_task.delay()  # type: ignore
        return comfort