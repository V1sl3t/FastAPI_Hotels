from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, check_date_to_after_date_from, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение отелей")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Адрес отеля"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(examples=["2024-08-01"]),
    date_to: date = Query(examples=["2024-08-10"]),
):
    return await HotelService(db).get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        pagination=pagination,
    )


@router.get("/{hotel_id}", summary="Получение отеля")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException


@router.post("", summary="Создание отеля")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Крым",
                "value": {
                    "title": "Черноморец",
                    "location": "Саки, ул.Морская 7",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Atlantis",
                    "location": "Дубай, dubai_palm",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление отеля")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частиное обновление отеля")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, hotel_id: int):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
