from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.message_enums import MessagePriority
import logging

logger = logging.getLogger(__name__)



class MessageBase(BaseModel):
    display_start: Optional[date] = None
    display_end: Optional[date] = None
    title: str
    message: str
    priority: MessagePriority


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    display_start: Optional[date] = None
    display_end: Optional[date] = None
    title: Optional[str] = None
    message: Optional[str] = None
    priority: Optional[MessagePriority] = None


class MessageInDBBase(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class Message(MessageInDBBase):
    pass
