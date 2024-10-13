from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение комнат")
@cache(expire=10)
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение комнаты")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание брони")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=400, detail="Бронирование не найдено")
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    new_booking_data = BookingAdd(price=room.price, user_id=user_id, **booking_data.model_dump())
    result = await db.bookings.add_booking(new_booking_data, hotel_id=hotel.id)
    await db.commit()

    return {"status": "OK", "data": result}
