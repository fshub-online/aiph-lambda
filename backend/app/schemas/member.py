from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    position: str
    email: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None
    supervisor_id: Optional[int] = None
    user_id: Optional[int] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    note: Optional[str] = None
    supervisor_id: Optional[int] = None
    user_id: Optional[int] = None

class MemberInDBBase(MemberBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

class Member(MemberInDBBase):
    pass
