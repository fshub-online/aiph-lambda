from sqlalchemy import Integer, String, Text, Date, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum

class ObjectivePriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class ObjectiveStatus(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    at_risk = "at_risk"
    on_hold = "on_hold"
    delayed = "delayed"
    completed = "completed"
    cancelled = "cancelled"

class Objective(Base):
    __tablename__ = "objective"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("objective.id"), nullable=True)
    priority: Mapped[ObjectivePriority] = mapped_column(Enum(ObjectivePriority), nullable=False, default=ObjectivePriority.medium)
    status: Mapped[ObjectiveStatus] = mapped_column(Enum(ObjectiveStatus), nullable=False, default=ObjectiveStatus.not_started)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    measurable_target: Mapped[str] = mapped_column(String(255), nullable=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # percent complete

    # Relationships
    parent = relationship("Objective", remote_side="Objective.id", backref="children")
    member = relationship("Member", back_populates="objectives")