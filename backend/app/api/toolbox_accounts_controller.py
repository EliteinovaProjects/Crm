from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.core.id_generator import generate_id

router = APIRouter(prefix="/toolbox/accounts", tags=["Toolbox Accounts"])


# Preferences
@router.get("/preferences")
def get_preferences(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get user preferences"""
    # This would typically retrieve preferences from a settings table
    return {
        "user_id": current_user.id,
        "theme": "light",
        "language": "en",
        "timezone": "UTC",
        "notifications_enabled": True
    }


@router.put("/preferences")
def update_preferences(
    theme: str = None,
    language: str = None,
    timezone: str = None,
    notifications_enabled: bool = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update user preferences"""
    # This would typically store preferences in a settings table
    return {
        "message": "Preferences updated successfully",
        "theme": theme,
        "language": language,
        "timezone": timezone,
        "notifications_enabled": notifications_enabled
    }


# Payment History
@router.get("/payment-history")
def get_payment_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get payment history"""
    from app.models.payment_history import PaymentHistory
    
    history = db.query(PaymentHistory).filter(
        PaymentHistory.user_id == current_user.id
    ).order_by(PaymentHistory.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": payment.id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "transaction_id": payment.transaction_id,
            "status": payment.status,
            "description": payment.description,
            "created_at": payment.created_at.isoformat()
        }
        for payment in history
    ]


# DID Configuration
@router.post("/did-config")
def create_did_number(
    phone_number: str,
    provider: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new DID number configuration"""
    from app.models.did import DIDNumber
    
    did = DIDNumber(
        id=generate_id("DID", 6),
        phone_number=phone_number,
        provider=provider
    )
    db.add(did)
    db.commit()
    db.refresh(did)
    
    return {
        "id": did.id,
        "phone_number": did.phone_number,
        "provider": did.provider,
        "is_active": did.is_active,
        "created_at": did.created_at.isoformat()
    }


@router.get("/did-config")
def get_did_numbers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all DID numbers"""
    from app.models.did import DIDNumber
    
    dids = db.query(DIDNumber).offset(skip).limit(limit).all()
    
    return [
        {
            "id": did.id,
            "phone_number": did.phone_number,
            "provider": did.provider,
            "is_active": did.is_active,
            "created_at": did.created_at.isoformat()
        }
        for did in dids
    ]


@router.put("/did-config/{did_id}")
def update_did_number(
    did_id: str,
    is_active: bool = None,
    provider: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update DID number configuration"""
    from app.models.did import DIDNumber
    
    did = db.query(DIDNumber).filter(DIDNumber.id == did_id).first()
    if not did:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DID number not found"
        )
    
    if is_active is not None:
        did.is_active = is_active
    if provider is not None:
        did.provider = provider
    
    db.commit()
    db.refresh(did)
    
    return {
        "id": did.id,
        "phone_number": did.phone_number,
        "provider": did.provider,
        "is_active": did.is_active,
        "updated_at": did.updated_at.isoformat()
    }


@router.delete("/did-config/{did_id}")
def delete_did_number(
    did_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete DID number"""
    from app.models.did import DIDNumber
    
    did = db.query(DIDNumber).filter(DIDNumber.id == did_id).first()
    if not did:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DID number not found"
        )
    
    db.delete(did)
    db.commit()
    
    return {"message": "DID number deleted successfully"}
