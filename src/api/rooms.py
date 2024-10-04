from fastapi import Query, APIRouter, Body

from src.repositories.rooms import RoomsRepository
from src.db import async_session_maker
from src.schemas.rooms import RoomPatch, RoomAdd

router = APIRouter(prefix="/hotels", tags=["Комнаты"])

@router.get("/{hotel_id}/rooms", summary="Получение комнат")
async def get_rooms(
        hotel_id: int,
        title: str | None = Query(None, description="Название вида комнаты"),
        price: int | None = Query(None, description="Цена вида комнаты")
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id,
            price = price,
            title = title,
        )


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты")
async def get_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Создание комнаты")
async def create_hotel(room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "BigHit",
        "value": {
            "hotel_id": 4,
            "title": "Big",
            "description": "very cool",
            "price": 1000,
            "quantity": 5

        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "hotel_id": 5,
            "title": "WWQQQ",
            "description": "top 1000",
            "price": 2000,
            "quantity": 8
        }
    }
})
):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление комнаты")
async def put_hotel(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частиное обновление комнаты")
async def patch_hotel(
        room_id: int,
        room_data: RoomPatch
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление комнаты")
async def delete_hotel(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}