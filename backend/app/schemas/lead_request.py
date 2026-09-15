from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class LeadBase(BaseModel):
    account: Optional[str] = None
    name: str = Field(..., min_length=1)
    mobile_number: str = Field(..., min_length=10)
    alternate_number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    source_id: Optional[str] = None
    status_id: Optional[str] = None
    category_id: Optional[str] = None
    follow_up_date: Optional[datetime] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(LeadBase):
    pass


class LeadBulkUpdate(BaseModel):
    lead_ids: List[str]
    update_type: str  # category, source
    update_value: str  # IVR In Bound, IVR Out Bound, etc.


class LeadAssign(BaseModel):
    lead_ids: List[str]
    agent_group_id: Optional[str] = None
    agent_ids: Optional[List[str]] = None


class LeadResponse(LeadBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LeadImportRequest(BaseModel):
    agent_id: Optional[str] = None
    source_id: Optional[str] = None
    status_id: Optional[str] = None
    category_id: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    restore_deleted: bool = False
    reassign_existing: bool = False


class LeadExportRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    agent_id: Optional[str] = None
    status_id: Optional[str] = None
    source_id: Optional[str] = None
    category_id: Optional[str] = None
