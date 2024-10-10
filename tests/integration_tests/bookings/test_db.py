from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)
    bookings = await db.bookings.get_all()
    booking_id = bookings[0].id
    booking_data.price = 1000
    await db.bookings.edit(booking_data, id=booking_id)
    await db.bookings.delete(id=booking_id)
    await db.commit()