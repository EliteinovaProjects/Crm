from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.lead import Lead
from app.models.user import User, UserRole
from app.models.call_log import CallLog


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def get_admin_dashboard_stats(self) -> Dict[str, Any]:
        # Total leads
        total_leads = self.db.query(Lead).filter(Lead.is_deleted == False).count()
        
        # Agent-wise leads allocation
        agent_wise = self.db.query(
            Lead.assigned_agent_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.assigned_agent_id.isnot(None)
        ).group_by(Lead.assigned_agent_id).all()
        
        agent_wise_dict = {}
        for agent_id, count in agent_wise:
            agent = self.db.query(User).filter(User.id == agent_id).first()
            agent_name = agent.full_name if agent else "Unknown"
            agent_wise_dict[agent_name] = count
        
        # Status-wise leads
        status_wise = self.db.query(
            Lead.status_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.status_id.isnot(None)
        ).group_by(Lead.status_id).all()
        
        status_wise_dict = {}
        for status_id, count in status_wise:
            from app.models.status import Status
            status = self.db.query(Status).filter(Status.id == status_id).first()
            status_name = status.status_name if status else "Unknown"
            status_wise_dict[status_name] = count
        
        # Source/Status leads
        source_status = self.db.query(
            Lead.source_id,
            Lead.status_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.source_id.isnot(None),
            Lead.status_id.isnot(None)
        ).group_by(Lead.source_id, Lead.status_id).all()
        
        source_status_dict = {}
        for source_id, status_id, count in source_status:
            from app.models.source import Source
            from app.models.status import Status
            source = self.db.query(Source).filter(Source.id == source_id).first()
            status = self.db.query(Status).filter(Status.id == status_id).first()
            source_name = source.source_name if source else "Unknown"
            status_name = status.status_name if status else "Unknown"
            key = f"{source_name}/{status_name}"
            source_status_dict[key] = count
        
        # Category/Status leads
        category_status = self.db.query(
            Lead.category_id,
            Lead.status_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.category_id.isnot(None),
            Lead.status_id.isnot(None)
        ).group_by(Lead.category_id, Lead.status_id).all()
        
        category_status_dict = {}
        for category_id, status_id, count in category_status:
            from app.models.category import Category
            from app.models.status import Status
            category = self.db.query(Category).filter(Category.id == category_id).first()
            status = self.db.query(Status).filter(Status.id == status_id).first()
            category_name = category.category_name if category else "Unknown"
            status_name = status.status_name if status else "Unknown"
            key = f"{category_name}/{status_name}"
            category_status_dict[key] = count
        
        # Source/Category leads
        source_category = self.db.query(
            Lead.source_id,
            Lead.category_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.source_id.isnot(None),
            Lead.category_id.isnot(None)
        ).group_by(Lead.source_id, Lead.category_id).all()
        
        source_category_dict = {}
        for source_id, category_id, count in source_category:
            from app.models.source import Source
            from app.models.category import Category
            source = self.db.query(Source).filter(Source.id == source_id).first()
            category = self.db.query(Category).filter(Category.id == category_id).first()
            source_name = source.source_name if source else "Unknown"
            category_name = category.category_name if category else "Unknown"
            key = f"{source_name}/{category_name}"
            source_category_dict[key] = count
        
        # Source-wise leads
        source_wise = self.db.query(
            Lead.source_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.source_id.isnot(None)
        ).group_by(Lead.source_id).all()

        source_wise_dict = {}
        for source_id, count in source_wise:
            from app.models.source import Source
            source = self.db.query(Source).filter(Source.id == source_id).first()
            source_name = source.source_name if source else "Unknown"
            source_wise_dict[source_name] = count

        # Category-wise leads
        category_wise = self.db.query(
            Lead.category_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.is_deleted == False,
            Lead.category_id.isnot(None)
        ).group_by(Lead.category_id).all()

        category_wise_dict = {}
        for category_id, count in category_wise:
            from app.models.category import Category
            category = self.db.query(Category).filter(Category.id == category_id).first()
            category_name = category.category_name if category else "Unknown"
            category_wise_dict[category_name] = count

        # Recent leads
        recent_leads = self.db.query(Lead).filter(
            Lead.is_deleted == False
        ).order_by(Lead.created_at.desc()).limit(10).all()
        
        recent_leads_data = [
            {
                "id": lead.id,
                "name": lead.name,
                "mobile_number": lead.mobile_number,
                "status": lead.status_id,
                "created_at": lead.created_at.isoformat()
            }
            for lead in recent_leads
        ]
        
        # Upcoming follow-ups
        today = datetime.utcnow().date()
        upcoming_followups = self.db.query(Lead).filter(
            Lead.is_deleted == False,
            Lead.follow_up_date >= today,
            Lead.follow_up_date <= today + timedelta(days=7)
        ).order_by(Lead.follow_up_date.asc()).limit(10).all()
        
        upcoming_followups_data = [
            {
                "id": lead.id,
                "name": lead.name,
                "mobile_number": lead.mobile_number,
                "follow_up_date": lead.follow_up_date.isoformat() if lead.follow_up_date else None
            }
            for lead in upcoming_followups
        ]
        
        return {
            "total_leads": total_leads,
            "agent_wise_leads": agent_wise_dict,
            "status_wise_leads": status_wise_dict,
            "source_wise_leads": source_wise_dict,
            "category_wise_leads": category_wise_dict,
            "recent_leads": recent_leads_data,
            "upcoming_followups": upcoming_followups_data
        }

    def get_employee_dashboard_stats(self, employee_id: str) -> Dict[str, Any]:
        # Total leads for employee
        total_leads = self.db.query(Lead).filter(
            Lead.assigned_agent_id == employee_id,
            Lead.is_deleted == False
        ).count()
        
        # My leads
        my_leads = total_leads
        
        # Status-wise leads for employee
        status_wise = self.db.query(
            Lead.status_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.assigned_agent_id == employee_id,
            Lead.is_deleted == False,
            Lead.status_id.isnot(None)
        ).group_by(Lead.status_id).all()
        
        status_wise_dict = {}
        for status_id, count in status_wise:
            from app.models.status import Status
            status = self.db.query(Status).filter(Status.id == status_id).first()
            status_name = status.status_name if status else "Unknown"
            status_wise_dict[status_name] = count
        
        # Source-wise leads for employee
        source_wise = self.db.query(
            Lead.source_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.assigned_agent_id == employee_id,
            Lead.is_deleted == False,
            Lead.source_id.isnot(None)
        ).group_by(Lead.source_id).all()
        
        source_wise_dict = {}
        for source_id, count in source_wise:
            from app.models.source import Source
            source = self.db.query(Source).filter(Source.id == source_id).first()
            source_name = source.source_name if source else "Unknown"
            source_wise_dict[source_name] = count
        
        # Category-wise leads for employee
        category_wise = self.db.query(
            Lead.category_id,
            func.count(Lead.id).label('count')
        ).filter(
            Lead.assigned_agent_id == employee_id,
            Lead.is_deleted == False,
            Lead.category_id.isnot(None)
        ).group_by(Lead.category_id).all()
        
        category_wise_dict = {}
        for category_id, count in category_wise:
            from app.models.category import Category
            category = self.db.query(Category).filter(Category.id == category_id).first()
            category_name = category.category_name if category else "Unknown"
            category_wise_dict[category_name] = count
        
        # Today's follow-ups
        today = datetime.utcnow().date()
        today_followups = self.db.query(Lead).filter(
            Lead.assigned_agent_id == employee_id,
            Lead.is_deleted == False,
            Lead.follow_up_date >= today,
            Lead.follow_up_date < today + timedelta(days=1)
        ).order_by(Lead.follow_up_date.asc()).all()
        
        today_followups_data = [
            {
                "id": lead.id,
                "name": lead.name,
                "mobile_number": lead.mobile_number,
                "follow_up_date": lead.follow_up_date.isoformat() if lead.follow_up_date else None
            }
            for lead in today_followups
        ]
        
        # Recent calls
        recent_calls = self.db.query(CallLog).filter(
            CallLog.agent_id == employee_id
        ).order_by(CallLog.started_at.desc()).limit(10).all()
        
        recent_calls_data = [
            {
                "id": call.id,
                "phone_number": call.phone_number,
                "call_direction": call.call_direction,
                "call_status": call.call_status,
                "duration": call.duration,
                "started_at": call.started_at.isoformat()
            }
            for call in recent_calls
        ]
        
        return {
            "total_leads": total_leads,
            "my_leads": my_leads,
            "status_wise_leads": status_wise_dict,
            "source_wise_leads": source_wise_dict,
            "category_wise_leads": category_wise_dict,
            "today_followups": today_followups_data,
            "recent_calls": recent_calls_data
        }
