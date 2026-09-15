from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class Disposition(Base):
    __tablename__ = "dispositions"
    
    id = Column(String, primary_key=True, index=True)
    disposition_name = Column(String, nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(String, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
