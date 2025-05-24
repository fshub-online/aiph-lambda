from pydantic import BaseModel
from typing import Optional, List
from datetime import date as _date, time as _time, datetime


class MeetingParticipantBase(BaseModel):
    meeting_id: int
    member_id: int


class MeetingParticipantCreate(BaseModel):
    member_id: int


class MeetingParticipantUpdate(BaseModel):
    meeting_id: Optional[int] = None
    member_id: Optional[int] = None


class MeetingParticipantInDBBase(MeetingParticipantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class MeetingParticipant(MeetingParticipantInDBBase):
    pass


class MeetingObjectiveBase(BaseModel):
    meeting_id: int
    objective_id: int
    note: Optional[str] = None


class MeetingObjectiveCreate(BaseModel):
    objective_id: int
    note: Optional[str] = None


class MeetingObjectiveUpdate(BaseModel):
    meeting_id: Optional[int] = None
    objective_id: Optional[int] = None
    note: Optional[str] = None


class MeetingObjectiveInDBBase(MeetingObjectiveBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class MeetingObjective(MeetingObjectiveInDBBase):
    pass


class MeetingKeyResultBase(BaseModel):
    meeting_id: int
    key_result_id: int
    note: Optional[str] = None


class MeetingKeyResultCreate(BaseModel):
    key_result_id: int
    note: Optional[str] = None


class MeetingKeyResultUpdate(BaseModel):
    meeting_id: Optional[int] = None
    key_result_id: Optional[int] = None
    note: Optional[str] = None


class MeetingKeyResultInDBBase(MeetingKeyResultBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class MeetingKeyResult(MeetingKeyResultInDBBase):
    pass


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
    pass


class MeetingWithIDs(MeetingInDBBase):
    participant_ids: List[int] = []
    objective_ids: List[int] = []
    key_result_ids: List[int] = []
