from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/check-in")
def check_in(
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check in for work"""
    attendance_service = AttendanceService(db)
    
    try:
        attendance = attendance_service.check_in(current_user.id, notes)
        return {
            "id": attendance.id,
            "user_id": attendance.user_id,
            "check_in_time": attendance.check_in_time.isoformat(),
            "status": attendance.status,
            "notes": attendance.notes
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/quick-check-in")
def quick_check_in(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick check in for work (simplified version for header button)"""
    from datetime import datetime
    
    # Existing users may have NULL status values from before attendance was added.
    current_status = current_user.current_status or "offline"
    if current_status in ("online", "on_break"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked in"
        )
    
    current_user.current_status = "online"
    current_user.last_check_in = datetime.utcnow()
    current_user.is_on_break = False
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": current_user.current_status,
        "last_check_in": current_user.last_check_in.isoformat(),
        "message": "Checked in successfully"
    }


@router.post("/quick-check-out")
def quick_check_out(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick check out from work (simplified version for header button)"""
    from datetime import datetime
    
    current_status = current_user.current_status or "offline"
    if current_status == "offline":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already checked out"
        )
    
    current_user.current_status = "offline"
    current_user.last_check_out = datetime.utcnow()
    current_user.is_on_break = False
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": current_user.current_status,
        "last_check_out": current_user.last_check_out.isoformat(),
        "message": "Checked out successfully"
    }


@router.post("/quick-break-start")
def quick_break_start(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick start break (simplified version for header button)"""
    from datetime import datetime
    
    if current_user.is_on_break:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already on break"
        )
    
    current_user.is_on_break = True
    current_user.break_start_time = datetime.utcnow()
    current_user.current_status = "on_break"
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": current_user.current_status,
        "is_on_break": current_user.is_on_break,
        "break_start_time": current_user.break_start_time.isoformat(),
        "message": "Break started successfully"
    }


@router.post("/quick-break-end")
def quick_break_end(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick end break (simplified version for header button)"""
    from datetime import datetime
    
    if not current_user.is_on_break:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not currently on break"
        )
    
    current_user.is_on_break = False
    current_user.break_start_time = None
    current_user.current_status = "online"
    current_user.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": current_user.current_status,
        "is_on_break": current_user.is_on_break,
        "message": "Break ended successfully"
    }


@router.post("/check-out")
def check_out(
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check out from work"""
    attendance_service = AttendanceService(db)
    
    try:
        attendance = attendance_service.check_out(current_user.id, notes)
        return {
            "id": attendance.id,
            "user_id": attendance.user_id,
            "check_in_time": attendance.check_in_time.isoformat(),
            "check_out_time": attendance.check_out_time.isoformat() if attendance.check_out_time else None,
            "status": attendance.status,
            "total_break_duration": attendance.total_break_duration,
            "notes": attendance.notes
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/break/start")
def start_break(
    break_reason_id: str,
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a break"""
    attendance_service = AttendanceService(db)
    
    try:
        break_record = attendance_service.start_break(current_user.id, break_reason_id, notes)
        return {
            "id": break_record.id,
            "attendance_id": break_record.attendance_id,
            "break_reason_id": break_record.break_reason_id,
            "start_time": break_record.start_time.isoformat(),
            "notes": break_record.notes
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/break/end")
def end_break(
    notes: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """End current break"""
    attendance_service = AttendanceService(db)
    
    try:
        break_record = attendance_service.end_break(current_user.id, notes)
        return {
            "id": break_record.id,
            "attendance_id": break_record.attendance_id,
            "break_reason_id": break_record.break_reason_id,
            "start_time": break_record.start_time.isoformat(),
            "end_time": break_record.end_time.isoformat() if break_record.end_time else None,
            "duration": break_record.duration,
            "notes": break_record.notes
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/current")
def get_current_attendance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current attendance status"""
    attendance_service = AttendanceService(db)
    attendance = attendance_service.get_current_attendance(current_user.id)
    
    if not attendance:
        return {
            "checked_in": False,
            "message": "No active check-in found"
        }
    
    return {
        "id": attendance.id,
        "user_id": attendance.user_id,
        "check_in_time": attendance.check_in_time.isoformat(),
        "check_out_time": attendance.check_out_time.isoformat() if attendance.check_out_time else None,
        "status": attendance.status,
        "total_break_duration": attendance.total_break_duration,
        "notes": attendance.notes
    }


@router.get("/current-break")
def get_current_break(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current break status"""
    attendance_service = AttendanceService(db)
    break_record = attendance_service.get_current_break(current_user.id)
    
    if not break_record:
        return {
            "on_break": False,
            "message": "No active break found"
        }
    
    return {
        "id": break_record.id,
        "attendance_id": break_record.attendance_id,
        "break_reason_id": break_record.break_reason_id,
        "start_time": break_record.start_time.isoformat(),
        "end_time": break_record.end_time.isoformat() if break_record.end_time else None,
        "duration": break_record.duration,
        "notes": break_record.notes
    }


@router.get("/history")
def get_attendance_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get attendance history"""
    attendance_service = AttendanceService(db)
    history = attendance_service.get_attendance_history(current_user.id, skip, limit)
    
    return [
        {
            "id": attendance.id,
            "user_id": attendance.user_id,
            "check_in_time": attendance.check_in_time.isoformat(),
            "check_out_time": attendance.check_out_time.isoformat() if attendance.check_out_time else None,
            "status": attendance.status,
            "total_break_duration": attendance.total_break_duration,
            "notes": attendance.notes,
            "created_at": attendance.created_at.isoformat()
        }
        for attendance in history
    ]


@router.get("/break-reasons")
def get_break_reasons(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get break reasons"""
    attendance_service = AttendanceService(db)
    reasons = attendance_service.get_break_reasons(skip, limit)
    
    return [
        {
            "id": reason.id,
            "reason_name": reason.reason_name,
            "description": reason.description,
            "is_active": reason.is_active,
            "created_at": reason.created_at.isoformat()
        }
        for reason in reasons
    ]


@router.post("/break-reasons")
def create_break_reason(
    reason_name: str,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new break reason (admin only in real implementation)"""
    attendance_service = AttendanceService(db)
    
    try:
        reason = attendance_service.create_break_reason({
            "reason_name": reason_name,
            "description": description
        })
        return {
            "id": reason.id,
            "reason_name": reason.reason_name,
            "description": reason.description,
            "is_active": reason.is_active,
            "created_at": reason.created_at.isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/today-summary")
def get_today_attendance_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get today's attendance summary"""
    attendance_service = AttendanceService(db)
    summary = attendance_service.get_today_attendance_summary(current_user.id)
    return summary


@router.put("/status")
def update_user_status(
    status: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user's current status (online, offline, on_break, ready_for_calls)"""
    from datetime import datetime
    
    valid_statuses = ["online", "offline", "on_break", "ready_for_calls"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    current_user.current_status = status
    
    if status == "online":
        current_user.last_check_in = datetime.utcnow()
        current_user.is_on_break = False
    elif status == "offline":
        current_user.last_check_out = datetime.utcnow()
        current_user.is_on_break = False
    elif status == "on_break":
        current_user.is_on_break = True
        current_user.break_start_time = datetime.utcnow()
    elif status == "ready_for_calls":
        current_user.is_on_break = False
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    
    return {
        "status": current_user.current_status,
        "last_check_in": current_user.last_check_in.isoformat() if current_user.last_check_in else None,
        "last_check_out": current_user.last_check_out.isoformat() if current_user.last_check_out else None,
        "is_on_break": current_user.is_on_break,
        "break_start_time": current_user.break_start_time.isoformat() if current_user.break_start_time else None
    }
