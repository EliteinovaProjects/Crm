from sqlalchemy import Column, String, DateTime, Integer, Text
from datetime import datetime
from app.core.database import Base


class SystemLog(Base):
    __tablename__ = "system_logs"
    
    id = Column(String, primary_key=True, index=True)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    user_id = Column(String)
    ip_address = Column(String)
    user_agent = Column(Text)
    status_code = Column(Integer, nullable=False)
    processing_time = Column(Integer)  # in milliseconds
    created_at = Column(DateTime, default=datetime.utcnow)
