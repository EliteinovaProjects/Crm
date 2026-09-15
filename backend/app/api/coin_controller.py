from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.coin_schemas import (
    CoinWalletResponse, CoinTransactionResponse, TopupRequest, TopupResponse, CoinStatsResponse
)
from app.services.coin_service import CoinService

router = APIRouter(prefix="/coins", tags=["Coins"])


@router.get("/wallet", response_model=CoinStatsResponse)
def get_coin_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's coin wallet and statistics"""
    coin_service = CoinService(db)
    wallet_info = coin_service.get_user_wallet(current_user.id)
    return CoinStatsResponse(**wallet_info)


@router.post("/topup")
def topup_coins(
    topup_data: TopupRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Top-up coins for user"""
    coin_service = CoinService(db)
    
    try:
        result = coin_service.topup_coins(
            current_user.id,
            topup_data.coin_type,
            topup_data.amount,
            topup_data.payment_method
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/deduct")
def deduct_coins(
    coin_type: str,
    amount: int,
    description: str,
    reference_id: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deduct coins from user's wallet"""
    coin_service = CoinService(db)
    
    try:
        result = coin_service.deduct_coins(
            current_user.id,
            coin_type,
            amount,
            description,
            reference_id
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/transactions")
def get_transaction_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's transaction history"""
    coin_service = CoinService(db)
    transactions = coin_service.get_transaction_history(current_user.id, skip, limit)
    return transactions


@router.get("/topup-history")
def get_topup_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's top-up history"""
    coin_service = CoinService(db)
    topups = coin_service.get_topup_history(current_user.id, skip, limit)
    return topups


@router.post("/reset-monthly")
def reset_monthly_coins(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reset monthly coins (admin only in real implementation)"""
    coin_service = CoinService(db)
    
    try:
        result = coin_service.reset_monthly_coins(current_user.id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
