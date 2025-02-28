from typing import List

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum

from .base import Base


class Weekday(Enum):
    EVERYDAY = "0"
    MONDAY = "1"
    TUESDAY = "2"
    WEDNESDAY = "3"
    THURSDAY = "4"
    FRIDAY = "5"
    SATURDAY = "6"
    SUNDAY = "7"
    ONE_TIME = "8"


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(length=64), nullable=True)
    reminders: Mapped[List["Reminder"]] = relationship(
        back_populates="user", lazy="selectin", order_by="Reminder.idpk.asc()"
    )


class Reminder(Base):
    __tablename__ = "reminders"

    idpk_user: Mapped[int] = mapped_column(ForeignKey("users.idpk"))
    user: Mapped["User"] = relationship(back_populates="reminders", lazy="selectin")
    message_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    message: Mapped[str] = mapped_column(String(length=4096), nullable=True)
    time_to_send: Mapped[str] = mapped_column(
        String(length=64), default=Weekday.EVERYDAY
    )
    repeat: Mapped[str] = mapped_column(String(length=64))
    is_set: Mapped[bool] = mapped_column(default=False)
