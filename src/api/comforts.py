from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.comforts import ComfortAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=10)
async def get_all_comforts(db: DBDep):
    return await db.comforts.get_all()


@router.post("", summary="Создание удобства")
async def create_comfort(db: DBDep, comfort_data: ComfortAdd):
    result = await db.comforts.add(comfort_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": result}
