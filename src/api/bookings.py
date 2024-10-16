from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    RoomNotFoundHTTPException,
    AllRoomsAreBookedException,
    RoomNotFoundException,
    AllRoomsAreBookedHTTPException,
)
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение комнат")
@cache(expire=10)
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()


@router.get("/me", summary="Получение комнаты")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("", summary="Создание брони")
async def create_booking(db: DBDep, user_id: UserIdDep, booking_data: BookingAddRequest):
    try:
        booking = await BookingService(db).create_booking(user_id, booking_data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status": "OK", "data": booking}
