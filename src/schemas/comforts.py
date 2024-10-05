from pydantic import BaseModel


class ComfortAdd(BaseModel):
    title: str


class Comfort(ComfortAdd):
    id: int