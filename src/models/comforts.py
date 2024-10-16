import typing

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.db import Base

if typing.TYPE_CHECKING:
    from src.models import RoomsOrm


class ComfortsOrm(Base):
    __tablename__ = "comforts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="comforts", secondary="rooms_comforts"
    )


class RoomsComfortsOrm(Base):
    __tablename__ = "rooms_comforts"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    comfort_id: Mapped[int] = mapped_column(ForeignKey("comforts.id"))
