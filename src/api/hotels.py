from fastapi import Query, APIRouter, Body

from repositories.hotels import HotelsRepository
from src.db import async_session_maker
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение отелей")
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


@router.get("/{hotel_id}", summary="Получение отеля")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("", summary="Создание отеля")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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


@router.put("/{hotel_id}", summary="Полное обновление отеля")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частиное обновление отеля")
async def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPatch
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}