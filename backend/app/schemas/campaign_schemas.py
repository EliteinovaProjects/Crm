from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CampaignBase(BaseModel):
    campaign_name: str = Field(..., min_length=1)
    campaign_type: str  # inbound, outbound, blended
    call_pacing_ratio: int = 1
    did_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    closure_at: Optional[datetime] = None
    working_hours_start: Optional[str] = None
    working_hours_end: Optional[str] = None
    retry_attempts: int = 3
    duration_between_retry: int = 300
    assignment_type: str  # agent_wise, group_wise
    schedule_days: Optional[str] = None  # JSON array
    save_to_contacts: bool = False
    first_call_strategy: Optional[str] = None


class CampaignCreate(CampaignBase):
    pass


class CampaignUpdate(CampaignBase):
    pass


class CampaignResponse(CampaignBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignBaseContact(BaseModel):
    contact_name: Optional[str] = None
    phone_number: str
    email: Optional[str] = None
    custom_data: Optional[str] = None


class CampaignBaseCreate(BaseModel):
    campaign_id: str
    contacts: List[CampaignBaseContact]


class CampaignBaseResponse(BaseModel):
    id: str
    campaign_id: str
    contact_name: Optional[str]
    phone_number: str
    email: Optional[str]
    custom_data: Optional[str]
    call_status: str
    call_attempts: int
    last_called_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignField(BaseModel):
    field_name: str
    field_type: str
    is_required: bool = False
    options: Optional[str] = None
