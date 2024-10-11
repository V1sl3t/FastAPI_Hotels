# ruff: noqa: E402

import json

from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.db import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *  # noqa
from httpx import AsyncClient

from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def upload_db(setup_db):
    with open("tests/mock_hotels.json.", encoding="utf-8") as hotels_file:
        hotels_data = json.load(hotels_file)
    with open("tests/mock_rooms.json.", encoding="utf-8") as rooms_file:
        rooms_data = json.load(rooms_file)
    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, upload_db):
    await ac.post("/auth/register", json={"email": "gg@qwe.com", "password": "1234"})


@pytest.fixture(scope="session")
async def authenticated_ac(ac, register_user):
    await ac.post("/auth/login", json={"email": "gg@qwe.com", "password": "1234"})
    assert ac.cookies["access_token"]
    yield ac
