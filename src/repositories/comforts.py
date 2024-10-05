from src.models.comforts import ComfortsOrm, RoomsComfortsOrm
from src.repositories.base import BaseRepository
from src.schemas.comforts import Comfort, RoomComfort


class ComfortsRepository(BaseRepository):
    model = ComfortsOrm
    schema = Comfort


class RoomsComfortsRepository(BaseRepository):
    model = RoomsComfortsOrm
    schema = RoomComfort