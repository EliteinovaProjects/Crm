from sqlalchemy import Column, String, DateTime
from datetime import datetime
from app.core.database import Base


class BreakReason(Base):
    __tablename__ = "break_reasons"
    
    id = Column(String, primary_key=True, index=True)
    reason_name = Column(String, nullable=False, unique=True)
    description = Column(String)
    is_active = Column(String, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
