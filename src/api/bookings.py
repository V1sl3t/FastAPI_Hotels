from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("", summary="Создание брони")
async def create_room(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    room_price = await db.rooms.get_one_or_none(id=booking_data.model_dump()["room_id"])
    new_room_data = BookingAdd(price=room_price.price, user_id=user_id, **booking_data.model_dump())
    result = await db.bookings.add(new_room_data)
    await db.commit()

    return {"status": "OK", "data": result}
