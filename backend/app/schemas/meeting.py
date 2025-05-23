from pydantic import BaseModel
from typing import Optional, List
from datetime import date as _date, time as _time, datetime


class MeetingParticipantBase(BaseModel):
    member_id: int


class MeetingParticipantCreate(MeetingParticipantBase):
    pass


class MeetingParticipant(MeetingParticipantBase):
    meeting_id: int

    class Config:
        from_attributes = True


class MeetingObjectiveBase(BaseModel):
    objective_id: int
    note: Optional[str] = None


class MeetingObjectiveCreate(MeetingObjectiveBase):
    pass


class MeetingObjective(MeetingObjectiveBase):
    meeting_id: int

    class Config:
        from_attributes = True


class MeetingKeyResultBase(BaseModel):
    key_result_id: int
    note: Optional[str] = None


class MeetingKeyResultCreate(MeetingKeyResultBase):
    pass


class MeetingKeyResult(MeetingKeyResultBase):
    meeting_id: int

    class Config:
        from_attributes = True


class MeetingBase(BaseModel):
    title: str
    date: _date
    time: _time
    duration: int
    minutes: Optional[str] = None
    lead_member_id: int


class MeetingCreate(MeetingBase):
    pass


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[_date] = None
    time: Optional[_time] = None
    duration: Optional[int] = None
    minutes: Optional[str] = None
    lead_member_id: Optional[int] = None


class MeetingInDBBase(MeetingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class Meeting(MeetingInDBBase):
    participants: List[MeetingParticipant] = []
    objectives: List[MeetingObjective] = []
    key_results: List[MeetingKeyResult] = []
