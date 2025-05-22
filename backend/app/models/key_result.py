from sqlalchemy import String, Text, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.key_result_enums import KeyResultStatus, KeyResultPriority, KeyResultComplexity

class KeyResult(Base):
    __tablename__ = "key_result"

    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)
    objective_id: Mapped[int | None] = mapped_column(ForeignKey("objective.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    value_definition: Mapped[str] = mapped_column(String(255), nullable=False)
    unit: Mapped[str] = mapped_column(String(64), nullable=False)
    start_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, nullable=False)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[KeyResultStatus] = mapped_column(Enum(KeyResultStatus), nullable=False, default=KeyResultStatus.current)
    priority: Mapped[KeyResultPriority] = mapped_column(Enum(KeyResultPriority), nullable=False, default=KeyResultPriority.medium)
    complexity: Mapped[KeyResultComplexity] = mapped_column(Enum(KeyResultComplexity), nullable=False, default=KeyResultComplexity.moderate)
    start_date: Mapped[Date] = mapped_column(Date, nullable=True)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)

    member = relationship("Member", back_populates="key_results", lazy="selectin")
    objective = relationship("Objective", back_populates="key_results", lazy="selectin")
