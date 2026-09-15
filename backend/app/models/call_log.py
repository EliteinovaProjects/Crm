from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CallLog(Base):
    __tablename__ = "call_logs"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("users.id"), nullable=False)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    phone_number = Column(String, nullable=False)
    call_direction = Column(String)  # inbound, outbound
    call_status = Column(String)  # ringing, connected, ended, failed
    duration = Column(Integer, default=0)  # in seconds
    recording_url = Column(String)
    disposition = Column(String)
    notes = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    # Relationships
    agent = relationship("User")
    lead = relationship("Lead")
