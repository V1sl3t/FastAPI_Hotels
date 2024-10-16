from pydantic import BaseModel


class ComfortAdd(BaseModel):
    title: str


class Comfort(ComfortAdd):
    id: int


class RoomComfortAdd(BaseModel):
    room_id: int
    comfort_id: int


class RoomComfort(RoomComfortAdd):
    id: int
