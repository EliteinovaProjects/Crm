from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.services.telephony_service import TelephonyService

router = APIRouter(prefix="/calls", tags=["Calls"])


@router.post("/initiate")
def initiate_call(
    phone_number: str,
    lead_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate a new call"""
    telephony_service = TelephonyService(db)
    
    try:
        call = telephony_service.initiate_call(current_user.id, phone_number, lead_id)
        return {
            "call_id": call.id,
            "phone_number": call.phone_number,
            "call_status": call.call_status,
            "started_at": call.started_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{call_id}/status")
def update_call_status(
    call_id: str,
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update call status"""
    telephony_service = TelephonyService(db)
    
    try:
        call = telephony_service.update_call_status(call_id, status)
        return {
            "call_id": call.id,
            "call_status": call.call_status,
            "updated_at": call.started_at.isoformat() if call.started_at else None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{call_id}/end")
def end_call(
    call_id: str,
    disposition: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End a call"""
    telephony_service = TelephonyService(db)
    
    try:
        call = telephony_service.end_call(call_id, disposition, notes)
        return {
            "call_id": call.id,
            "call_status": call.call_status,
            "duration": call.duration,
            "disposition": call.disposition,
            "ended_at": call.ended_at.isoformat() if call.ended_at else None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/{call_id}")
def get_call_log(
    call_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get call log by ID"""
    telephony_service = TelephonyService(db)
    call = telephony_service.get_call_log(call_id)
    
    if not call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found"
        )
    
    # Users can only see their own calls
    if call.agent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this call"
        )
    
    return {
        "id": call.id,
        "agent_id": call.agent_id,
        "lead_id": call.lead_id,
        "phone_number": call.phone_number,
        "call_direction": call.call_direction,
        "call_status": call.call_status,
        "duration": call.duration,
        "disposition": call.disposition,
        "notes": call.notes,
        "started_at": call.started_at.isoformat() if call.started_at else None,
        "ended_at": call.ended_at.isoformat() if call.ended_at else None
    }


@router.get("/agent/me")
def get_my_calls(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's calls"""
    telephony_service = TelephonyService(db)
    calls = telephony_service.get_agent_calls(current_user.id, skip, limit)
    
    return [
        {
            "id": call.id,
            "phone_number": call.phone_number,
            "call_direction": call.call_direction,
            "call_status": call.call_status,
            "duration": call.duration,
            "disposition": call.disposition,
            "started_at": call.started_at.isoformat() if call.started_at else None,
            "ended_at": call.ended_at.isoformat() if call.ended_at else None
        }
        for call in calls
    ]


@router.get("/lead/{lead_id}")
def get_lead_calls(
    lead_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get calls for a specific lead"""
    telephony_service = TelephonyService(db)
    calls = telephony_service.get_lead_calls(lead_id, skip, limit)
    
    return [
        {
            "id": call.id,
            "agent_id": call.agent_id,
            "phone_number": call.phone_number,
            "call_direction": call.call_direction,
            "call_status": call.call_status,
            "duration": call.duration,
            "disposition": call.disposition,
            "started_at": call.started_at.isoformat() if call.started_at else None,
            "ended_at": call.ended_at.isoformat() if call.ended_at else None
        }
        for call in calls
    ]


@router.get("/stats/{agent_id}")
def get_call_stats(
    agent_id: str,
    start_date: str,
    end_date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get call statistics for an agent"""
    from datetime import datetime
    
    telephony_service = TelephonyService(db)
    
    # Users can only see their own stats unless they're admin
    if current_user.role.value != "admin" and current_user.id != agent_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these stats"
        )
    
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        stats = telephony_service.get_call_stats(agent_id, start_dt, end_dt)
        return stats
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format"
        )


@router.put("/agent/status")
def update_agent_status(
    status: str,
    mode: str = "available",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update agent status"""
    telephony_service = TelephonyService(db)
    result = telephony_service.update_agent_status(current_user.id, status, mode)
    return result


@router.put("/agent/campaign-ready")
def set_campaign_ready(
    ready: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set agent ready for campaign calls"""
    telephony_service = TelephonyService(db)
    result = telephony_service.set_agent_ready_for_campaign(current_user.id, ready)
    return result
