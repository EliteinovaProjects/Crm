from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.call_log import CallLog
from app.core.id_generator import generate_id


class TelephonyService:
    def __init__(self, db: Session):
        self.db = db

    def initiate_call(self, agent_id: str, phone_number: str, lead_id: Optional[str] = None) -> CallLog:
        call_log = CallLog(
            id=generate_id("CALL", 6),
            agent_id=agent_id,
            lead_id=lead_id,
            phone_number=phone_number,
            call_direction="outbound",
            call_status="ringing",
            started_at=datetime.utcnow()
        )
        self.db.add(call_log)
        self.db.commit()
        self.db.refresh(call_log)
        return call_log

    def update_call_status(self, call_id: str, status: str) -> CallLog:
        call = self.db.query(CallLog).filter(CallLog.id == call_id).first()
        if not call:
            raise ValueError("Call not found")
        
        call.call_status = status
        if status == "connected":
            call.started_at = datetime.utcnow()
        elif status in ["ended", "failed"]:
            call.ended_at = datetime.utcnow()
            if call.started_at:
                call.duration = int((call.ended_at - call.started_at).total_seconds())
        
        self.db.commit()
        self.db.refresh(call)
        return call

    def end_call(self, call_id: str, disposition: Optional[str] = None, notes: Optional[str] = None) -> CallLog:
        call = self.db.query(CallLog).filter(CallLog.id == call_id).first()
        if not call:
            raise ValueError("Call not found")
        
        call.call_status = "ended"
        call.ended_at = datetime.utcnow()
        if call.started_at:
            call.duration = int((call.ended_at - call.started_at).total_seconds())
        if disposition:
            call.disposition = disposition
        if notes:
            call.notes = notes
        
        self.db.commit()
        self.db.refresh(call)
        return call

    def get_call_log(self, call_id: str) -> Optional[CallLog]:
        return self.db.query(CallLog).filter(CallLog.id == call_id).first()

    def get_agent_calls(self, agent_id: str, skip: int = 0, limit: int = 100) -> List[CallLog]:
        return self.db.query(CallLog).filter(
            CallLog.agent_id == agent_id
        ).order_by(CallLog.started_at.desc()).offset(skip).limit(limit).all()

    def get_lead_calls(self, lead_id: str, skip: int = 0, limit: int = 100) -> List[CallLog]:
        return self.db.query(CallLog).filter(
            CallLog.lead_id == lead_id
        ).order_by(CallLog.started_at.desc()).offset(skip).limit(limit).all()

    def get_call_stats(self, agent_id: str, start_date: datetime, end_date: datetime) -> dict:
        calls = self.db.query(CallLog).filter(
            CallLog.agent_id == agent_id,
            CallLog.started_at >= start_date,
            CallLog.started_at <= end_date
        ).all()
        
        total_calls = len(calls)
        connected_calls = len([c for c in calls if c.call_status == "ended"])
        total_duration = sum([c.duration for c in calls if c.duration])
        
        return {
            "total_calls": total_calls,
            "connected_calls": connected_calls,
            "total_duration": total_duration,
            "average_duration": total_duration / connected_calls if connected_calls > 0 else 0
        }

    def update_agent_status(self, agent_id: str, status: str, mode: str = "available") -> dict:
        # This would typically update agent status in a real-time system
        # For now, we'll return a status update
        return {
            "agent_id": agent_id,
            "status": status,
            "mode": mode,
            "updated_at": datetime.utcnow().isoformat()
        }

    def set_agent_ready_for_campaign(self, agent_id: str, ready: bool) -> dict:
        return {
            "agent_id": agent_id,
            "ready_for_campaign": ready,
            "updated_at": datetime.utcnow().isoformat()
        }
