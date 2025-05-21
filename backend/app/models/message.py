from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Date
from datetime import date
from app.db.base import Base


class Message(Base):
    __tablename__ = "message"
    display_start: Mapped[date | None] = mapped_column(
        Date, unique=False, index=False, nullable=True
    )
    display_end: Mapped[date | None] = mapped_column(
        Date, unique=False, index=False, nullable=True
    )
    title: Mapped[str | None] = mapped_column(Text, nullable=False)
    message: Mapped[str | None] = mapped_column(Text, nullable=False)
