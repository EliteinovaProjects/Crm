from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CoinWallet(Base):
    __tablename__ = "coin_wallets"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    inbound_coins = Column(Integer, default=0)
    outbound_coins = Column(Integer, default=0)
    sms_coins = Column(Integer, default=0)
    email_coins = Column(Integer, default=0)
    fax_coins = Column(Integer, default=0)
    common_coins = Column(Integer, default=0)
    last_reset_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User")
    transactions = relationship("CoinTransaction", back_populates="wallet", cascade="all, delete-orphan")
