from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from app.models.coin_wallet import CoinWallet
from app.models.coin_transaction import CoinTransaction
from app.models.topup_history import TopupHistory


class CoinRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_wallet_by_user(self, user_id: str) -> Optional[CoinWallet]:
        return self.db.query(CoinWallet).filter(CoinWallet.user_id == user_id).first()

    def create_wallet(self, user_id: str) -> CoinWallet:
        wallet = CoinWallet(user_id=user_id)
        self.db.add(wallet)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def get_or_create_wallet(self, user_id: str) -> CoinWallet:
        wallet = self.get_wallet_by_user(user_id)
        if not wallet:
            wallet = self.create_wallet(user_id)
        return wallet

    def update_wallet(self, wallet: CoinWallet, coin_type: str, amount: int, transaction_type: str) -> CoinWallet:
        if transaction_type == "credit":
            setattr(wallet, f"{coin_type}_coins", getattr(wallet, f"{coin_type}_coins") + amount)
        else:  # debit
            current_amount = getattr(wallet, f"{coin_type}_coins")
            if current_amount < amount:
                raise ValueError(f"Insufficient {coin_type} coins")
            setattr(wallet, f"{coin_type}_coins", current_amount - amount)
        
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def reset_monthly_coins(self, wallet: CoinWallet) -> CoinWallet:
        wallet.inbound_coins = 0
        wallet.outbound_coins = 0
        wallet.sms_coins = 0
        wallet.email_coins = 0
        wallet.fax_coins = 0
        wallet.common_coins = 0
        wallet.last_reset_date = datetime.utcnow()
        self.db.commit()
        self.db.refresh(wallet)
        return wallet

    def check_monthly_reset(self, wallet: CoinWallet) -> bool:
        if not wallet.last_reset_date:
            return True
        # Check if it's been a month since last reset
        return datetime.utcnow() - wallet.last_reset_date >= timedelta(days=30)

    def create_transaction(self, wallet_id: str, transaction_data: dict) -> CoinTransaction:
        transaction = CoinTransaction(wallet_id=wallet_id, **transaction_data)
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_wallet_transactions(self, wallet_id: str, skip: int = 0, limit: int = 100) -> List[CoinTransaction]:
        return self.db.query(CoinTransaction).filter(
            CoinTransaction.wallet_id == wallet_id
        ).order_by(CoinTransaction.created_at.desc()).offset(skip).limit(limit).all()

    def create_topup(self, user_id: str, topup_data: dict) -> TopupHistory:
        topup = TopupHistory(user_id=user_id, **topup_data)
        self.db.add(topup)
        self.db.commit()
        self.db.refresh(topup)
        return topup

    def get_user_topups(self, user_id: str, skip: int = 0, limit: int = 100) -> List[TopupHistory]:
        return self.db.query(TopupHistory).filter(
            TopupHistory.user_id == user_id
        ).order_by(TopupHistory.created_at.desc()).offset(skip).limit(limit).all()

    def get_total_topup_by_type(self, user_id: str, coin_type: str) -> int:
        total = self.db.query(TopupHistory).filter(
            TopupHistory.user_id == user_id,
            TopupHistory.coin_type == coin_type,
            TopupHistory.status == "completed"
        ).with_entities(
            self.db.func.sum(TopupHistory.amount)
        ).scalar()
        return total or 0

    def get_available_balance(self, wallet: CoinWallet) -> Dict[str, int]:
        return {
            "inbound": wallet.inbound_coins,
            "outbound": wallet.outbound_coins,
            "sms": wallet.sms_coins,
            "email": wallet.email_coins,
            "fax": wallet.fax_coins,
            "common": wallet.common_coins
        }
