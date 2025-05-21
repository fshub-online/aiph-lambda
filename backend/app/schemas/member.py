from pydantic import BaseModel
from typing import Optional

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

class MemberUpdate(MemberBase):
    pass

class MemberInDBBase(MemberBase):
    id: int
    class Config:
        from_attributes = True

class Member(MemberInDBBase):
    pass
