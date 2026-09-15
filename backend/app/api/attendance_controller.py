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
