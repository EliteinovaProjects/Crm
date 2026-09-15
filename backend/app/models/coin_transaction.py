from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CoinTransaction(Base):
    __tablename__ = "coin_transactions"
    
    id = Column(String, primary_key=True, index=True)
    wallet_id = Column(String, ForeignKey("coin_wallets.id"), nullable=False)
    transaction_type = Column(String, nullable=False)  # credit, debit
    coin_type = Column(String, nullable=False)  # inbound, outbound, sms, email, fax, common
    amount = Column(Integer, nullable=False)
    description = Column(Text)
    reference_id = Column(String)  # can reference call_id, campaign_id, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    wallet = relationship("CoinWallet", back_populates="transactions")
