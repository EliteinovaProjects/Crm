from sqlalchemy import Column, String, DateTime, Integer, Text
from datetime import datetime
from app.core.database import Base


class TopupHistory(Base):
    __tablename__ = "topup_history"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    coin_type = Column(String, nullable=False)  # inbound, outbound, sms, email, fax, common
    amount = Column(Integer, nullable=False)
    payment_method = Column(String)
    transaction_id = Column(String)
    status = Column(String)  # pending, completed, failed
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
