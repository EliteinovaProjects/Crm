from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
from app.core.database import Base


class DIDNumber(Base):
    __tablename__ = "did_numbers"
    
    id = Column(String, primary_key=True, index=True)
    phone_number = Column(String, nullable=False, unique=True)
    provider = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
