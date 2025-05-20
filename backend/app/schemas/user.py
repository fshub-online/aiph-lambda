from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    user_name: str
    first_name: str
    last_name: str
    position: Optional[str] = None
    notes: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    notes: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
