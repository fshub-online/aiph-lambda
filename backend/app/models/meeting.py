from sqlalchemy import String, Text, Date, Time, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
import logging

logger = logging.getLogger(__name__)



# Association table for meeting participants
class MeetingParticipant(Base):
    __tablename__ = "meeting_participant"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))


# Association table for meeting-objective with note
class MeetingObjective(Base):
    __tablename__ = "meeting_objective"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"))
    objective_id: Mapped[int] = mapped_column(ForeignKey("objective.id"))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    # id will be inherited from Base as the primary key


# Association table for meeting-key_result with note
class MeetingKeyResult(Base):
    __tablename__ = "meeting_key_result"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meeting.id"))
    key_result_id: Mapped[int] = mapped_column(ForeignKey("key_result.id"))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    # id will be inherited from Base as the primary key


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

