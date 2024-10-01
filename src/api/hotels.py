from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func

from repositories.hotels import HotelsRepository
from src.db import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelPatch, Hotel
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location = location,
            title = title,
            limit=pagination.per_page,
            offset=pagination.per_page * (pagination.page - 1)
        )


@router.delete("/{hotel_id}", summary="Удаление")
async def delete_hotel(
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля")
):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(
            location=location,
            title=title,
        )
        await session.commit()
    return {"status": "OK"}


@router.post("", summary="Создание")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Крым",
        "value": {
            "title": "Черноморец",
            "location": "Саки, ул.Морская 7",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Atlantis",
            "location": "Дубай, dubai_palm",
        }
    }
})
):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": result}


@router.put("/{hotel_id}", summary="Полное обновление")
async def put_hotel(
        hotel_data: Hotel,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data,
            location = location,
            title = title
        )
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частиное обновление")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    if hotel_data.title:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name:
        hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}