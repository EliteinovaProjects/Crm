from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole


class AgentBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None


class AgentCreate(AgentBase):
    password: str
    role: UserRole = UserRole.EMPLOYEE
    group_ids: Optional[List[str]] = None


class AgentUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    group_ids: Optional[List[str]] = None


class AgentResponse(AgentBase):
    id: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentGroupBase(BaseModel):
    group_name: str = Field(..., min_length=1)
    description: Optional[str] = None


class AgentGroupCreate(AgentGroupBase):
    pass


class AgentGroupUpdate(AgentGroupBase):
    pass


class AgentGroupResponse(AgentGroupBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
