from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum
from app.core.database import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    SUB_ADMIN = "sub_admin"
    EMPLOYEE = "employee"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Attendance tracking fields for employees
    last_check_in = Column(DateTime, nullable=True)
    last_check_out = Column(DateTime, nullable=True)
    is_on_break = Column(Boolean, default=False)
    break_start_time = Column(DateTime, nullable=True)
    current_status = Column(String, default="offline")  # online, offline, on_break, ready_for_calls
    
    # Relationships
    leads = relationship("Lead", back_populates="assigned_agent")
    attendance = relationship("Attendance", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
