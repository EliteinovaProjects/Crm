from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.notification import Notification
from app.core.id_generator import generate_id
from app.core.websocket_manager import manager


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    async def create_notification(self, user_id: str, notification_data: dict) -> Notification:
        notification_data["id"] = generate_id("NTF", 6)
        notification_data["user_id"] = user_id
        notification = Notification(**notification_data)
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        # Send real-time notification via WebSocket
        await manager.send_personal_message({
            "type": "notification",
            "data": {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "notification_type": notification.notification_type,
                "action_url": notification.action_url,
                "created_at": notification.created_at.isoformat()
            }
        }, user_id)
        
        return notification

    def get_notification(self, notification_id: str) -> Optional[Notification]:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_user_notifications(self, user_id: str, skip: int = 0, limit: int = 100, unread_only: bool = False) -> List[Notification]:
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()

    def mark_as_read(self, notification_id: str) -> Notification:
        notification = self.get_notification(notification_id)
        if not notification:
            raise ValueError("Notification not found")
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def mark_all_as_read(self, user_id: str) -> int:
        notifications = self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).all()
        
        count = 0
        for notification in notifications:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            count += 1
        
        self.db.commit()
        return count

    def delete_notification(self, notification_id: str) -> bool:
        notification = self.get_notification(notification_id)
        if not notification:
            raise ValueError("Notification not found")
        
        self.db.delete(notification)
        self.db.commit()
        return True

    def get_unread_count(self, user_id: str) -> int:
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()

    async def send_lead_notification(self, user_id: str, lead_id: str, message: str):
        await self.create_notification(user_id, {
            "title": "New Lead Assigned",
            "message": message,
            "notification_type": "lead",
            "action_url": f"/leads/{lead_id}"
        })

    async def send_call_notification(self, user_id: str, call_id: str, message: str):
        await self.create_notification(user_id, {
            "title": "Call Update",
            "message": message,
            "notification_type": "call",
            "action_url": f"/calls/{call_id}"
        })

    async def send_reminder_notification(self, user_id: str, reminder_id: str, message: str):
        await self.create_notification(user_id, {
            "title": "Reminder",
            "message": message,
            "notification_type": "reminder",
            "action_url": f"/reminders/{reminder_id}"
        })

    async def send_system_notification(self, user_id: str, title: str, message: str):
        await self.create_notification(user_id, {
            "title": title,
            "message": message,
            "notification_type": "system",
            "action_url": None
        })
