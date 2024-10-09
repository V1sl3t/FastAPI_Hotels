import json

import pytest

from src.config import settings
from src.db import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from httpx import AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def upload_db(setup_db):
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open('tests/mock_hotels.json.', 'r') as file:
            hotels_data = json.load(file)
            for hotel in hotels_data:
                await db.hotels.add(HotelAdd.model_validate(hotel))
        with open('tests/mock_rooms.json.', 'r') as file:
            rooms_data = json.load(file)
            for room in rooms_data:
                await db.rooms.add(RoomAdd.model_validate(room))
        await db.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(upload_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "gg@qwe.com",
                "password": "1234"
            }
        )
