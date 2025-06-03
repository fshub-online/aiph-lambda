from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey
from app.db.base import Base
import logging

logger = logging.getLogger(__name__)


class Member(Base):
    __tablename__ = "member"
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    supervisor_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("member.id"), nullable=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)

    supervisor = relationship("Member", remote_side="Member.id", backref="subordinates", lazy="selectin")
    user = relationship("User", backref="member_profile", lazy="selectin")
    objectives = relationship("Objective", back_populates="member", lazy="selectin")
    # key_results relationship will be set after KeyResult is defined

# Set key_results relationship after KeyResult is defined to avoid circular import
try:
    Member.key_results = relationship("KeyResult", back_populates="member", lazy="selectin")
except ImportError:
    pass
