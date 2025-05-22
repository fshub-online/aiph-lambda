from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.key_result import KeyResultStatus, KeyResultPriority, KeyResultComplexity

class KeyResultBase(BaseModel):
    member_id: int
    objective_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    value_definition: str
    unit: str
    start_value: float
    current_value: float
    target_value: float
    status: KeyResultStatus = KeyResultStatus.current
    priority: KeyResultPriority = KeyResultPriority.medium
    complexity: KeyResultComplexity = KeyResultComplexity.moderate
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class KeyResultCreate(KeyResultBase):
    pass

class KeyResultUpdate(BaseModel):
    member_id: Optional[int] = None
    objective_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    value_definition: Optional[str] = None
    unit: Optional[str] = None
    start_value: Optional[float] = None
    current_value: Optional[float] = None
    target_value: Optional[float] = None
    status: Optional[KeyResultStatus] = None
    priority: Optional[KeyResultPriority] = None
    complexity: Optional[KeyResultComplexity] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class KeyResultInDBBase(KeyResultBase):
    id: int
    created_at: date
    updated_at: date
    
    class Config:
        from_attributes = True

class KeyResult(KeyResultInDBBase):
    pass
