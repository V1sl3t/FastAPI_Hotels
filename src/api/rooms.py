from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение комнат")
async def get_rooms(db: DBDep, hotel_id: int):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение комнаты")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Создание комнаты")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
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
    new_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    result = await db.rooms.add(new_room_data)
    await db.commit()

    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление комнаты")
async def put_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAdd):
    new_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(new_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частиное обновление комнаты")
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    new_room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(new_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление комнаты")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}