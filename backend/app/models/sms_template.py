from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class SMSTemplate(Base):
    __tablename__ = "sms_templates"
    
    id = Column(String, primary_key=True, index=True)
    template_name = Column(String, nullable=False, unique=True)
    template_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
