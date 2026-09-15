from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True, index=True)
    account = Column(String)
    name = Column(String, nullable=False)
    mobile_number = Column(String, nullable=False, index=True)
    alternate_number = Column(String)
    email = Column(String)
    address = Column(Text)
    description = Column(Text)
    
    # Relations
    assigned_agent_id = Column(String, ForeignKey("users.id"), nullable=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=True)
    status_id = Column(String, ForeignKey("statuses.id"), nullable=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    
    # Dates
    follow_up_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    
    # Relationships
    assigned_agent = relationship("User", back_populates="leads")
    source = relationship("Source", back_populates="leads")
    status = relationship("Status", back_populates="leads")
    category = relationship("Category", back_populates="leads")
    field_values = relationship("LeadFieldValue", back_populates="lead", cascade="all, delete-orphan")
