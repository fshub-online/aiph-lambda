from sqlalchemy import String, Text, Date, Time, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


# Association table for meeting participants
class MeetingParticipant(Base):
    __tablename__ = "meeting_participant"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), primary_key=True)


# Association table for meeting-objective with note
class MeetingObjective(Base):
    __tablename__ = "meeting_objective"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), primary_key=True)
    objective_id: Mapped[int] = mapped_column(
        ForeignKey("objective.id"), primary_key=True
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


# Association table for meeting-key_result with note
class MeetingKeyResult(Base):
    __tablename__ = "meeting_key_result"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"), primary_key=True)
    key_result_id: Mapped[int] = mapped_column(
        ForeignKey("key_result.id"), primary_key=True
    )
    note: Mapped[str | None] = mapped_column(Text, nullable=True)


class Meeting(Base):
    __tablename__ = "meeting"
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    time: Mapped[Time] = mapped_column(Time, nullable=False)
    duration: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # duration in minutes
    minutes: Mapped[str | None] = mapped_column(Text, nullable=True)
    lead_member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=False)

    lead_member = relationship("Member", foreign_keys=[lead_member_id], lazy="selectin")
    participants = relationship(
        "Member",
        secondary="meeting_participant",
        lazy="selectin",
        backref="meetings_participated",
    )
    objectives = relationship(
        "MeetingObjective",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    key_results = relationship(
        "MeetingKeyResult",
        back_populates="meeting",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


# Add back_populates to association models
MeetingObjective.meeting = relationship(
    "Meeting", back_populates="objectives", lazy="selectin"
)
MeetingObjective.objective = relationship("Objective", lazy="selectin")
MeetingKeyResult.meeting = relationship(
    "Meeting", back_populates="key_results", lazy="selectin"
)
MeetingKeyResult.key_result = relationship("KeyResult", lazy="selectin")
