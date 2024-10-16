from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.comforts import ComfortAdd
from src.services.comforts import ComfortService

router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("", summary="Получение удобств")
@cache(expire=10)
async def get_all_comforts(db: DBDep):
    return await ComfortService(db).get_all_comforts()


@router.post("", summary="Создание удобства")
async def create_comfort(db: DBDep, comfort_data: ComfortAdd):
    comfort = await ComfortService(db).create_comfort(comfort_data)
    return {"status": "OK", "data": comfort}
