from sqlalchemy import Column, String, DateTime, Integer, Text
from datetime import datetime
from app.core.database import Base


class RenewalHistory(Base):
    __tablename__ = "renewal_history"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    plan_type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    payment_method = Column(String)
    transaction_id = Column(String)
    status = Column(String)  # pending, completed, failed
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
