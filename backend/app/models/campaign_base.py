from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CampaignBase(Base):
    __tablename__ = "campaign_bases"
    
    id = Column(String, primary_key=True, index=True)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    contact_name = Column(String)
    phone_number = Column(String, nullable=False)
    email = Column(String)
    custom_data = Column(Text)  # JSON string for additional fields
    call_status = Column(String, default="pending")  # pending, called, completed
    call_attempts = Column(Integer, default=0)
    last_called_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="campaign_bases")
