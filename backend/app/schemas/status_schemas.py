from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StatusBase(BaseModel):
    status_name: str = Field(..., min_length=1)


class StatusCreate(StatusBase):
    pass


class StatusUpdate(StatusBase):
    pass


class StatusResponse(StatusBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
