from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.attendance import Attendance, Break
from app.models.break_reason import BreakReason
from app.core.id_generator import generate_id


class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    def check_in(self, user_id: str, notes: Optional[str] = None) -> Attendance:
        # Check if user already has an active attendance
        active_attendance = self.db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == "active"
        ).first()
        
        if active_attendance:
            raise ValueError("User already has an active check-in")
        
        attendance = Attendance(
            id=generate_id("ATT", 6),
            user_id=user_id,
            check_in_time=datetime.utcnow(),
            status="active",
            notes=notes
        )
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def check_out(self, user_id: str, notes: Optional[str] = None) -> Attendance:
        attendance = self.db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == "active"
        ).first()
        
        if not attendance:
            raise ValueError("No active check-in found for user")
        
        attendance.check_out_time = datetime.utcnow()
        attendance.status = "completed"
        if notes:
            attendance.notes = notes
        
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def start_break(self, user_id: str, break_reason_id: str, notes: Optional[str] = None) -> Break:
        # Get active attendance
        attendance = self.db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == "active"
        ).first()
        
        if not attendance:
            raise ValueError("No active check-in found for user")
        
        # Check if user already has an active break
        active_break = self.db.query(Break).filter(
            Break.attendance_id == attendance.id,
            Break.end_time.is_(None)
        ).first()
        
        if active_break:
            raise ValueError("User already has an active break")
        
        break_record = Break(
            id=generate_id("BRK", 6),
            attendance_id=attendance.id,
            break_reason_id=break_reason_id,
            start_time=datetime.utcnow(),
            notes=notes
        )
        self.db.add(break_record)
        self.db.commit()
        self.db.refresh(break_record)
        return break_record

    def end_break(self, user_id: str, notes: Optional[str] = None) -> Break:
        # Get active attendance
        attendance = self.db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == "active"
        ).first()
        
        if not attendance:
            raise ValueError("No active check-in found for user")
        
        # Get active break
        break_record = self.db.query(Break).filter(
            Break.attendance_id == attendance.id,
            Break.end_time.is_(None)
        ).first()
        
        if not break_record:
            raise ValueError("No active break found for user")
        
        break_record.end_time = datetime.utcnow()
        break_record.duration = int((break_record.end_time - break_record.start_time).total_seconds() / 60)  # in minutes
        if notes:
            break_record.notes = notes
        
        # Update total break duration in attendance
        attendance.total_break_duration += break_record.duration
        
        self.db.commit()
        self.db.refresh(break_record)
        return break_record

    def get_current_attendance(self, user_id: str) -> Optional[Attendance]:
        return self.db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == "active"
        ).first()

    def get_current_break(self, user_id: str) -> Optional[Break]:
        attendance = self.get_current_attendance(user_id)
        if not attendance:
            return None
        
        return self.db.query(Break).filter(
            Break.attendance_id == attendance.id,
            Break.end_time.is_(None)
        ).first()

    def get_attendance_history(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Attendance]:
        return self.db.query(Attendance).filter(
            Attendance.user_id == user_id
        ).order_by(Attendance.check_in_time.desc()).offset(skip).limit(limit).all()

    def get_break_reasons(self, skip: int = 0, limit: int = 100) -> List[BreakReason]:
        return self.db.query(BreakReason).filter(
            BreakReason.is_active == True
        ).offset(skip).limit(limit).all()

    def create_break_reason(self, reason_data: dict) -> BreakReason:
        reason_data["id"] = generate_id("BRR", 6)
        break_reason = BreakReason(**reason_data)
        self.db.add(break_reason)
        self.db.commit()
        self.db.refresh(break_reason)
        return break_reason

    def get_today_attendance_summary(self, user_id: str) -> dict:
        today = datetime.utcnow().date()
        attendance = self.db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_in_time >= today,
            Attendance.check_in_time < today + timedelta(days=1)
        ).first()
        
        if not attendance:
            return {
                "checked_in": False,
                "check_in_time": None,
                "check_out_time": None,
                "total_break_duration": 0,
                "current_break": None
            }
        
        current_break = self.get_current_break(user_id)
        
        return {
            "checked_in": attendance.status == "active",
            "check_in_time": attendance.check_in_time.isoformat(),
            "check_out_time": attendance.check_out_time.isoformat() if attendance.check_out_time else None,
            "total_break_duration": attendance.total_break_duration,
            "current_break": {
                "id": current_break.id,
                "reason_id": current_break.break_reason_id,
                "start_time": current_break.start_time.isoformat()
            } if current_break else None
        }
