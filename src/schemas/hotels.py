from pydantic import BaseModel


class HotelAdd(BaseModel):
    title: str
    location: str


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
