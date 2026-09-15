from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    check_in_time = Column(DateTime, nullable=False)
    check_out_time = Column(DateTime, nullable=True)
    total_break_duration = Column(Integer, default=0)  # in minutes
    status = Column(String, default="active")  # active, completed
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="attendance")
    breaks = relationship("Break", back_populates="attendance", cascade="all, delete-orphan")


class Break(Base):
    __tablename__ = "breaks"
    
    id = Column(String, primary_key=True, index=True)
    attendance_id = Column(String, ForeignKey("attendance.id"), nullable=False)
    break_reason_id = Column(String, ForeignKey("break_reasons.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, default=0)  # in minutes
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attendance = relationship("Attendance", back_populates="breaks")
