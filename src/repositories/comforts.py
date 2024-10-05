from src.models.comforts import ComfortsOrm
from src.repositories.base import BaseRepository
from src.schemas.comforts import Comfort


class ComfortsRepository(BaseRepository):
    model = ComfortsOrm
    schema = Comfort