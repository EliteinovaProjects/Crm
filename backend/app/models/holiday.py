from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class Holiday(Base):
    __tablename__ = "holidays"
    
    id = Column(String, primary_key=True, index=True)
    holiday_name = Column(String, nullable=False)
    holiday_date = Column(DateTime, nullable=False)
    description = Column(Text)
    is_recurring = Column(String, default=False)  # yearly, monthly, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
