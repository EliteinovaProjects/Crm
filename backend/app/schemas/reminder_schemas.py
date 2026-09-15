from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ReminderBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    reminder_date: datetime


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    reminder_date: Optional[datetime] = None
    is_completed: Optional[bool] = None


class ReminderResponse(ReminderBase):
    id: str
    user_id: str
    is_completed: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReminderListResponse(BaseModel):
    upcoming: list[ReminderResponse]
    history: list[ReminderResponse]
