from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.core.database import Base


class FieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    EMAIL = "email"
    DATE = "date"
    SELECT = "select"
    MULTISELECT = "multiselect"
    TEXTAREA = "textarea"
    CHECKBOX = "checkbox"


class LeadField(Base):
    __tablename__ = "lead_fields"
    
    id = Column(String, primary_key=True, index=True)
    field_name = Column(String, nullable=False)
    field_type = Column(String, nullable=False)
    is_required = Column(Boolean, default=False)
    options = Column(Text)  # JSON string for select/multiselect options
    placeholder = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    field_values = relationship("LeadFieldValue", back_populates="field", cascade="all, delete-orphan")


class LeadFieldValue(Base):
    __tablename__ = "lead_field_values"
    
    id = Column(String, primary_key=True, index=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    field_id = Column(String, ForeignKey("lead_fields.id"), nullable=False)
    value = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="field_values")
    field = relationship("LeadField", back_populates="field_values")
