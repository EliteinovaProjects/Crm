from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CoinWalletBase(BaseModel):
    inbound_coins: int = 0
    outbound_coins: int = 0
    sms_coins: int = 0
    email_coins: int = 0
    fax_coins: int = 0
    common_coins: int = 0


class CoinWalletResponse(CoinWalletBase):
    id: str
    user_id: str
    last_reset_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CoinTransactionBase(BaseModel):
    transaction_type: str  # credit, debit
    coin_type: str  # inbound, outbound, sms, email, fax, common
    amount: int = Field(..., gt=0)
    description: Optional[str] = None
    reference_id: Optional[str] = None


class CoinTransactionResponse(CoinTransactionBase):
    id: str
    wallet_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class TopupRequest(BaseModel):
    coin_type: str  # inbound, outbound, sms, email, fax, common
    amount: int = Field(..., gt=0)
    payment_method: Optional[str] = None


class TopupResponse(BaseModel):
    id: str
    user_id: str
    coin_type: str
    amount: int
    payment_method: Optional[str]
    transaction_id: Optional[str]
    status: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class CoinStatsResponse(BaseModel):
    monthly_coins: CoinWalletResponse
    total_topup: dict
    available_balance: dict
