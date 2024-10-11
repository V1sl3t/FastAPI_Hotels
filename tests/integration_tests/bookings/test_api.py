import pytest

from src.db import async_session_maker_null_pool
from src.utils.db_manager import DBManager


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-02", "2024-08-11", 200),
    (1, "2024-08-03", "2024-08-12", 200),
    (1, "2024-08-04", "2024-08-13", 200),
    (1, "2024-08-05", "2024-08-14", 200),
    (1, "2024-08-06", "2024-08-15", 500),
    (1, "2024-08-17", "2024-08-25", 200),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="session")
async def delete_all_bookings():
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        bookings = await db_.bookings.get_all()
        for booking in bookings:
            await db_.bookings.delete(id=booking.id)
        await db_.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, bookings_quantity", [
    (1, "2024-08-01", "2024-08-10", 200, 1),
    (1, "2024-08-02", "2024-08-11", 200, 2),
    (1, "2024-08-03", "2024-08-12", 200, 3)
])
async def test_add_and_get_bookings (
        room_id, date_from, date_to, status_code, bookings_quantity,
        db, authenticated_ac, delete_all_bookings
):
    await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    response = await authenticated_ac.get("/bookings/me")
    if response.status_code == status_code:
        res = response.json()
        assert isinstance(res, list)
        assert len(res) == bookings_quantity



