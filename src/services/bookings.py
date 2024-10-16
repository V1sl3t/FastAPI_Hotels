from src.exceptions import ObjectNotFoundException, RoomNotFoundException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, user_id: int, booking_data: BookingAddRequest):
        try:
            room: Room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel: Hotel = await self.db.hotels.get_one(id=room.hotel_id)
        new_booking_data = BookingAdd(
            price=room.price, user_id=user_id, **booking_data.model_dump()
        )
        booking = await self.db.bookings.add_booking(new_booking_data, hotel_id=hotel.id)
        await self.db.commit()

        return booking
