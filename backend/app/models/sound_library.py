from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime
from app.core.database import Base


class SoundLibrary(Base):
    __tablename__ = "sound_library"
    
    id = Column(String, primary_key=True, index=True)
    sound_name = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    description = Column(Text)
    duration = Column(String)  # in seconds or MM:SS format
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
