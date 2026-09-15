from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class Blacklist(Base):
    __tablename__ = "blacklist"
    
    id = Column(String, primary_key=True, index=True)
    phone_number = Column(String, nullable=False, unique=True)
    reason = Column(Text)
    blocked_by = Column(String)  # user id
    created_at = Column(DateTime, default=datetime.utcnow)
