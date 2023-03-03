import datetime as _datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(32))
    time: Mapped[_datetime.datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"User(uuid={self.uuid!r}, time={self.time!r})"


class Dialog(Base):

    __tablename__ = "dialog"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(32))
    time: Mapped[_datetime.datetime] = mapped_column(DateTime)
    who: Mapped[int]
    msg: Mapped[str]
    control_msg: Mapped[bool]
    received: Mapped[bool]

    def __repr__(self):
        return f"Dialog(uuid={self.uuid!r}, time={self.time!r}, who={self.who!r}, msg={self.msg!r}, control_msg={self.control_msg!r}, received={self.received!r})"
