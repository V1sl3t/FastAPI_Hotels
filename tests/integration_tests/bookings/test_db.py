from datetime import date

from src.schemas.bookings import BookingAdd, Booking
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id  # type: ignore
    room_id = (await db.rooms.get_all())[0].id  # type: ignore
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    new_booking: Booking = await db.bookings.add(booking_data)
    booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)

    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.user_id == new_booking.user_id
    assert (
        booking.model_dump(exclude={"id"}) == booking_data.model_dump()
    )  # одновременно все параметры

    updated_date = date(year=2024, month=8, day=25)
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=updated_date,
        price=100,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)

    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == updated_date

    await db.bookings.delete(id=new_booking.id)
    booking: Booking | None = await db.bookings.get_one_or_none(id=new_booking.id)

    assert not booking
