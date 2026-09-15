from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.lead_field import FieldType


class LeadFieldBase(BaseModel):
    field_name: str = Field(..., min_length=1)
    field_type: FieldType
    is_required: bool = False
    options: Optional[str] = None
    placeholder: Optional[str] = None


class LeadFieldCreate(LeadFieldBase):
    pass


class LeadFieldUpdate(LeadFieldBase):
    pass


class LeadFieldResponse(LeadFieldBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadFieldValueBase(BaseModel):
    lead_id: str
    field_id: str
    value: Optional[str] = None


class LeadFieldValueResponse(LeadFieldValueBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
