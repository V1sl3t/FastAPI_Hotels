from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.comforts import ComfortAdd


router = APIRouter(prefix="/comforts", tags=["Удобства"])


@router.get("", summary="Получение удобств")
async def get_all_comforts(db: DBDep):
    return await db.comforts.get_all()


@router.post("", summary="Создание удобства")
async def create_comfort(db: DBDep, comfort_data: ComfortAdd):
    result = await db.comforts.add(comfort_data)
    await db.commit()

    return {"status": "OK", "data": result}
