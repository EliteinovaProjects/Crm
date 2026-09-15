from typing import Optional, Dict
from sqlalchemy.orm import Session
from app.repositories.coin_repository import CoinRepository
from app.core.id_generator import generate_id


class CoinService:
    def __init__(self, db: Session):
        self.db = db
        self.coin_repository = CoinRepository(db)

    def get_user_wallet(self, user_id: str) -> Dict:
        wallet = self.coin_repository.get_or_create_wallet(user_id)
        
        # Check if monthly reset is needed
        if self.coin_repository.check_monthly_reset(wallet):
            wallet = self.coin_repository.reset_monthly_coins(wallet)
        
        available_balance = self.coin_repository.get_available_balance(wallet)
        total_topup = {}
        
        for coin_type in ["inbound", "outbound", "sms", "email", "fax", "common"]:
            total_topup[coin_type] = self.coin_repository.get_total_topup_by_type(user_id, coin_type)
        
        return {
            "wallet": {
                "id": wallet.id,
                "user_id": wallet.user_id,
                "inbound_coins": wallet.inbound_coins,
                "outbound_coins": wallet.outbound_coins,
                "sms_coins": wallet.sms_coins,
                "email_coins": wallet.email_coins,
                "fax_coins": wallet.fax_coins,
                "common_coins": wallet.common_coins,
                "last_reset_date": wallet.last_reset_date.isoformat() if wallet.last_reset_date else None
            },
            "total_topup": total_topup,
            "available_balance": available_balance
        }

    def topup_coins(self, user_id: str, coin_type: str, amount: int, payment_method: Optional[str] = None) -> Dict:
        wallet = self.coin_repository.get_or_create_wallet(user_id)
        
        # Create topup history
        topup_data = {
            "id": generate_id("TP", 6),
            "coin_type": coin_type,
            "amount": amount,
            "payment_method": payment_method,
            "status": "completed",
            "description": f"Top-up {coin_type} coins"
        }
        
        topup = self.coin_repository.create_topup(user_id, topup_data)
        
        # Credit coins to wallet
        self.coin_repository.update_wallet(wallet, coin_type, amount, "credit")
        
        # Create transaction record
        transaction_data = {
            "id": generate_id("TXN", 6),
            "transaction_type": "credit",
            "coin_type": coin_type,
            "amount": amount,
            "description": f"Top-up {coin_type} coins",
            "reference_id": topup.id
        }
        
        updated_wallet = self.coin_repository.get_wallet_by_user(user_id)
        self.coin_repository.create_transaction(updated_wallet.id, transaction_data)
        
        return {
            "success": True,
            "topup_id": topup.id,
            "coin_type": coin_type,
            "amount": amount,
            "new_balance": getattr(updated_wallet, f"{coin_type}_coins")
        }

    def deduct_coins(self, user_id: str, coin_type: str, amount: int, description: str, reference_id: Optional[str] = None) -> Dict:
        wallet = self.coin_repository.get_or_create_wallet(user_id)
        
        try:
            # Debit coins from wallet
            updated_wallet = self.coin_repository.update_wallet(wallet, coin_type, amount, "debit")
            
            # Create transaction record
            transaction_data = {
                "id": generate_id("TXN", 6),
                "transaction_type": "debit",
                "coin_type": coin_type,
                "amount": amount,
                "description": description,
                "reference_id": reference_id
            }
            
            self.coin_repository.create_transaction(updated_wallet.id, transaction_data)
            
            return {
                "success": True,
                "coin_type": coin_type,
                "amount": amount,
                "remaining_balance": getattr(updated_wallet, f"{coin_type}_coins")
            }
        except ValueError as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_transaction_history(self, user_id: str, skip: int = 0, limit: int = 100) -> list:
        wallet = self.coin_repository.get_wallet_by_user(user_id)
        if not wallet:
            return []
        
        transactions = self.coin_repository.get_wallet_transactions(wallet.id, skip, limit)
        return [
            {
                "id": txn.id,
                "transaction_type": txn.transaction_type,
                "coin_type": txn.coin_type,
                "amount": txn.amount,
                "description": txn.description,
                "reference_id": txn.reference_id,
                "created_at": txn.created_at.isoformat()
            }
            for txn in transactions
        ]

    def get_topup_history(self, user_id: str, skip: int = 0, limit: int = 100) -> list:
        topups = self.coin_repository.get_user_topups(user_id, skip, limit)
        return [
            {
                "id": topup.id,
                "coin_type": topup.coin_type,
                "amount": topup.amount,
                "payment_method": topup.payment_method,
                "transaction_id": topup.transaction_id,
                "status": topup.status,
                "description": topup.description,
                "created_at": topup.created_at.isoformat()
            }
            for topup in topups
        ]

    def reset_monthly_coins(self, user_id: str) -> Dict:
        wallet = self.coin_repository.get_or_create_wallet(user_id)
        updated_wallet = self.coin_repository.reset_monthly_coins(wallet)
        
        return {
            "success": True,
            "message": "Monthly coins reset successfully",
            "reset_date": updated_wallet.last_reset_date.isoformat()
        }
