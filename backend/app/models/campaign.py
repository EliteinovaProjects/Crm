from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, index=True)
    campaign_name = Column(String, nullable=False)
    campaign_type = Column(String, nullable=False)  # inbound, outbound, blended
    call_pacing_ratio = Column(Integer, default=1)
    did_id = Column(String, ForeignKey("did_numbers.id"))
    scheduled_at = Column(DateTime)
    closure_at = Column(DateTime)
    working_hours_start = Column(String)  # HH:MM format
    working_hours_end = Column(String)  # HH:MM format
    retry_attempts = Column(Integer, default=3)
    duration_between_retry = Column(Integer, default=300)  # in seconds
    assignment_type = Column(String)  # agent_wise, group_wise
    schedule_days = Column(Text)  # JSON array of days
    save_to_contacts = Column(Boolean, default=False)
    first_call_strategy = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    did = relationship("DIDNumber")
    campaign_bases = relationship("CampaignBase", back_populates="campaign", cascade="all, delete-orphan")
