from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)



class UserBase(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    notes: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    notes: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class UserPasswordChange(BaseModel):
    current_password: str
    new_password: str


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
