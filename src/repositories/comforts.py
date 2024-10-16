from typing import Sequence

from sqlalchemy import select, delete, insert

from src.models.comforts import ComfortsOrm, RoomsComfortsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import ComfortDataMapper
from src.schemas.comforts import RoomComfort


class ComfortsRepository(BaseRepository):
    model = ComfortsOrm
    mapper = ComfortDataMapper


class RoomsComfortsRepository(BaseRepository):
    model: RoomsComfortsOrm = RoomsComfortsOrm
    schema = RoomComfort

    async def set_room_comforts(self, room_id: int, comforts_ids: list[int]) -> None:
        get_current_comforts_ids = select(self.model.comfort_id).filter_by(room_id=room_id)
        res = await self.session.execute(get_current_comforts_ids)
        current_comforts_ids: Sequence[int] = res.scalars().all()
        ids_to_delete: list[int] = list(set(current_comforts_ids) - set(comforts_ids))
        ids_to_insert: list[int] = list(set(comforts_ids) - set(current_comforts_ids))
        if ids_to_delete:
            delete_rooms_comforts = delete(self.model).filter( # type: ignore
                self.model.room_id == room_id, self.model.comfort_id.in_(ids_to_delete) # type: ignore
            )
            await self.session.execute(delete_rooms_comforts)
        if ids_to_insert:
            insert_rooms_comforts = insert(self.model).values( # type: ignore
                [{"room_id": room_id, "comfort_id": f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_rooms_comforts)
