from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class MessageBase(BaseModel):
    display_start: Optional[date] = None
    display_end: Optional[date] = None
    title: str
    message: str


class MessageCreate(MessageBase):
    pass


class MessageUpdate(MessageBase):
    pass


class MessageInDBBase(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Message(MessageInDBBase):
    pass
