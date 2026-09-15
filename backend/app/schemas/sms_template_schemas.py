from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SMSTemplateBase(BaseModel):
    template_name: str = Field(..., min_length=1)
    template_content: str = Field(..., min_length=1)


class SMSTemplateCreate(SMSTemplateBase):
    pass


class SMSTemplateUpdate(SMSTemplateBase):
    pass


class SMSTemplateResponse(SMSTemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
