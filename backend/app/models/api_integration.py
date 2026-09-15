from sqlalchemy import Column, String, DateTime, Text, Boolean
from datetime import datetime
from app.core.database import Base


class APIIntegration(Base):
    __tablename__ = "api_integrations"
    
    id = Column(String, primary_key=True, index=True)
    integration_name = Column(String, nullable=False)
    api_key = Column(String, nullable=False)
    api_secret = Column(String, nullable=False)
    endpoint_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
