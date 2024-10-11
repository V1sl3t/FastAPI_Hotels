from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UniqueConstraint

from src.db import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(200))

    __table_args__ = (UniqueConstraint("email"),)
