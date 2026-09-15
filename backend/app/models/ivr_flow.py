from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class IVRFlow(Base):
    __tablename__ = "ivr_flows"
    
    id = Column(String, primary_key=True, index=True)
    flow_name = Column(String, nullable=False)
    flow_config = Column(Text, nullable=False)  # JSON string representing the IVR flow
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
