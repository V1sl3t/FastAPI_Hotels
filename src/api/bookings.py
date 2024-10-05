from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение комнат")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение комнаты")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Создание брони")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    new_booking_data = BookingAdd(price=room.price, user_id=user_id, **booking_data.model_dump())
    result = await db.bookings.add(new_booking_data)
    await db.commit()

    return {"status": "OK", "data": result}
