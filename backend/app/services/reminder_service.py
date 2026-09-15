from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.reminder import Reminder
from app.core.id_generator import generate_id


class ReminderService:
    def __init__(self, db: Session):
        self.db = db

    def create_reminder(self, user_id: str, reminder_data: dict) -> Reminder:
        reminder_data["id"] = generate_id("RMD", 6)
        reminder_data["user_id"] = user_id
        reminder = Reminder(**reminder_data)
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        return self.db.query(Reminder).filter(Reminder.id == reminder_id).first()

    def get_user_reminders(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Reminder]:
        return self.db.query(Reminder).filter(
            Reminder.user_id == user_id
        ).order_by(Reminder.reminder_date.asc()).offset(skip).limit(limit).all()

    def get_upcoming_reminders(self, user_id: str, limit: int = 10) -> List[Reminder]:
        now = datetime.utcnow()
        return self.db.query(Reminder).filter(
            Reminder.user_id == user_id,
            Reminder.is_completed == False,
            Reminder.reminder_date >= now
        ).order_by(Reminder.reminder_date.asc()).limit(limit).all()

    def get_reminder_history(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Reminder]:
        return self.db.query(Reminder).filter(
            Reminder.user_id == user_id,
            Reminder.is_completed == True
        ).order_by(Reminder.completed_at.desc()).offset(skip).limit(limit).all()

    def update_reminder(self, reminder_id: str, reminder_data: dict) -> Reminder:
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            raise ValueError("Reminder not found")
        
        for key, value in reminder_data.items():
            if hasattr(reminder, key) and value is not None:
                setattr(reminder, key, value)
        
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def complete_reminder(self, reminder_id: str) -> Reminder:
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            raise ValueError("Reminder not found")
        
        reminder.is_completed = True
        reminder.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(reminder)
        return reminder

    def delete_reminder(self, reminder_id: str) -> bool:
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            raise ValueError("Reminder not found")
        
        self.db.delete(reminder)
        self.db.commit()
        return True

    def get_reminders_summary(self, user_id: str) -> dict:
        upcoming = self.get_upcoming_reminders(user_id)
        history = self.get_reminder_history(user_id, limit=10)
        
        return {
            "upcoming_count": len(upcoming),
            "history_count": len(history),
            "upcoming": [
                {
                    "id": r.id,
                    "title": r.title,
                    "description": r.description,
                    "reminder_date": r.reminder_date.isoformat()
                }
                for r in upcoming
            ],
            "history": [
                {
                    "id": r.id,
                    "title": r.title,
                    "description": r.description,
                    "reminder_date": r.reminder_date.isoformat(),
                    "completed_at": r.completed_at.isoformat() if r.completed_at else None
                }
                for r in history
            ]
        }
