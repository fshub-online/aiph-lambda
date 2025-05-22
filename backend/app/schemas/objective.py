from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.models.objective import ObjectivePriority, ObjectiveStatus

class ObjectiveBase(BaseModel):
    title: str
    description: Optional[str] = None
    member_id: int
    parent_id: Optional[int] = None
    priority: ObjectivePriority = ObjectivePriority.medium
    status: ObjectiveStatus = ObjectiveStatus.not_started
    start_date: date
    end_date: date
    measurable_target: Optional[str] = None
    progress: int = 0

class ObjectiveCreate(ObjectiveBase):
    pass

class ObjectiveUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    member_id: Optional[int] = None
    parent_id: Optional[int] = None
    priority: Optional[ObjectivePriority] = None
    status: Optional[ObjectiveStatus] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    measurable_target: Optional[str] = None
    progress: Optional[int] = None

class ObjectiveInDBBase(ObjectiveBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat(),
        }

class Objective(ObjectiveInDBBase):
    pass

