from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.comforts import RoomComfort, RoomComfortAdd
from src.schemas.rooms import RoomPatch, RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms", summary="Получение комнат")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


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
    rooms_comforts_data = [RoomComfortAdd(room_id=result.id, comfort_id=f_id) for f_id in room_data.comforts_ids]
    await db.rooms_comforts.add_bulk(rooms_comforts_data)
    await db.commit()

    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное обновление комнаты")
async def put_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    new_room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(new_room_data, id=room_id)
    await db.rooms_comforts.set_room_comforts(room_id=room_id, comforts_ids=room_data.comforts_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частиное обновление комнаты")
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    room_data_dict = room_data.model_dump(exclude_unset=True)
    new_room_data = RoomPatch(hotel_id=hotel_id, **room_data_dict)
    await db.rooms.edit(new_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    if "comforts_ids" in room_data_dict:
        await db.rooms_comforts.set_room_comforts(room_id=room_id, comforts_ids=room_data_dict["comforts_ids"])
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление комнаты")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}