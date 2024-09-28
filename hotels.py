from fastapi import Query, APIRouter, Body
from schemas.hotels import HotelPatch, Hotel


router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", summary="Получение")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(default=1),
        per_page: int | None = Query(default=3),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[per_page*(page-1):per_page*page]


@router.delete("/{hotel_id}", summary="Удаление")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Создание")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
        }
    }
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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