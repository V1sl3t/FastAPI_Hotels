from datetime import date

from fastapi import Query, APIRouter, Body

from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получение отелей")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}", summary="Получение отеля")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Создание отеля")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    result = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": result}


@router.put("/{hotel_id}", summary="Полное обновление отеля")
async def put_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частиное обновление отеля")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatch
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}