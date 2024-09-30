from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select

from src.db import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import HotelPatch, Hotel
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.contains(location))
        if title:
            query = query.filter(HotelsOrm.title.contains(title))
        query = (
            query
            .limit(pagination.per_page)
            .offset(pagination.per_page * (pagination.page-1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels



@router.delete("/{hotel_id}", summary="Удаление")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Создание")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Крым",
        "value": {
            "title": "Черноморец",
            "location": "Саки, ул.Морская 7",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Atlantis",
            "location": "Дубай, dubai_palm",
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Полное обновление")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частиное обновление")
def patch_hotel(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    if hotel_data.title:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name:
        hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}