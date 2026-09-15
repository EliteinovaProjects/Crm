from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    email = Column(String)
    address = Column(Text)
    company = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
