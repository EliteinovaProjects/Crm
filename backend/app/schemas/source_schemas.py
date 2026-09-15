from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SourceBase(BaseModel):
    lead_type: str = Field(..., min_length=1)
    source_name: str = Field(..., min_length=1)


class SourceCreate(SourceBase):
    pass


class SourceUpdate(SourceBase):
    pass


class SourceResponse(SourceBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
