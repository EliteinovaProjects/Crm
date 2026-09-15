from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class LeadFieldValueResponse(BaseModel):
    id: str
    field_id: str
    value: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeadDetailResponse(BaseModel):
    id: str
    account: Optional[str]
    name: str
    mobile_number: str
    alternate_number: Optional[str]
    email: Optional[str]
    address: Optional[str]
    description: Optional[str]
    assigned_agent_id: Optional[str]
    source_id: Optional[str]
    status_id: Optional[str]
    category_id: Optional[str]
    follow_up_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime]
    field_values: List[LeadFieldValueResponse] = []

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    leads: List[LeadDetailResponse]
    total: int
    page: int
    page_size: int


class LeadStatsResponse(BaseModel):
    total_leads: int
    agent_wise_allocation: dict
    status_wise_leads: dict
    source_status_leads: dict
    category_status_leads: dict
    source_category_leads: dict
