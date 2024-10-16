from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager


async def test_add_hotel(db: DBManager):
    hotel_data = HotelAdd(title="Hotel 5 stars", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()
