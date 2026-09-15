from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.lead import Lead
from app.models.lead_field import LeadFieldValue


class LeadRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lead_id: str) -> Optional[Lead]:
        return self.db.query(Lead).filter(Lead.id == lead_id).first()

    def get_by_mobile(self, mobile_number: str) -> Optional[Lead]:
        return self.db.query(Lead).filter(
            Lead.mobile_number == mobile_number,
            Lead.is_deleted == False
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100, include_deleted: bool = False) -> List[Lead]:
        query = self.db.query(Lead)
        if not include_deleted:
            query = query.filter(Lead.is_deleted == False)
        return query.offset(skip).limit(limit).all()

    def get_by_agent(self, agent_id: str, skip: int = 0, limit: int = 100) -> List[Lead]:
        return self.db.query(Lead).filter(
            Lead.assigned_agent_id == agent_id,
            Lead.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_by_status(self, status_id: str, skip: int = 0, limit: int = 100) -> List[Lead]:
        return self.db.query(Lead).filter(
            Lead.status_id == status_id,
            Lead.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_by_source(self, source_id: str, skip: int = 0, limit: int = 100) -> List[Lead]:
        return self.db.query(Lead).filter(
            Lead.source_id == source_id,
            Lead.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_by_category(self, category_id: str, skip: int = 0, limit: int = 100) -> List[Lead]:
        return self.db.query(Lead).filter(
            Lead.category_id == category_id,
            Lead.is_deleted == False
        ).offset(skip).limit(limit).all()

    def get_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Lead]:
        return self.db.query(Lead).filter(
            Lead.created_at >= start_date,
            Lead.created_at <= end_date,
            Lead.is_deleted == False
        ).offset(skip).limit(limit).all()

    def create(self, lead_data: dict) -> Lead:
        db_lead = Lead(**lead_data)
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead

    def bulk_create(self, leads_data: List[dict]) -> List[Lead]:
        db_leads = [Lead(**lead_data) for lead_data in leads_data]
        self.db.add_all(db_leads)
        self.db.commit()
        for lead in db_leads:
            self.db.refresh(lead)
        return db_leads

    def update(self, lead: Lead, lead_data: dict) -> Lead:
        for key, value in lead_data.items():
            if hasattr(lead, key) and value is not None:
                setattr(lead, key, value)
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def bulk_update(self, lead_ids: List[str], update_data: dict) -> List[Lead]:
        leads = self.db.query(Lead).filter(Lead.id.in_(lead_ids)).all()
        for lead in leads:
            for key, value in update_data.items():
                if hasattr(lead, key) and value is not None:
                    setattr(lead, key, value)
        self.db.commit()
        for lead in leads:
            self.db.refresh(lead)
        return leads

    def soft_delete(self, lead: Lead) -> Lead:
        lead.is_deleted = True
        lead.deleted_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def restore(self, lead: Lead) -> Lead:
        lead.is_deleted = False
        lead.deleted_at = None
        self.db.commit()
        self.db.refresh(lead)
        return lead

    def get_stats(self) -> Dict[str, Any]:
        total_leads = self.db.query(Lead).filter(Lead.is_deleted == False).count()
        
        # Agent-wise allocation
        agent_wise = {}
        for lead in self.db.query(Lead).filter(Lead.is_deleted == False).all():
            agent_id = lead.assigned_agent_id or "unassigned"
            agent_wise[agent_id] = agent_wise.get(agent_id, 0) + 1
        
        # Status-wise
        status_wise = {}
        for lead in self.db.query(Lead).filter(Lead.is_deleted == False).all():
            status_id = lead.status_id or "no_status"
            status_wise[status_id] = status_wise.get(status_id, 0) + 1
        
        return {
            "total_leads": total_leads,
            "agent_wise_allocation": agent_wise,
            "status_wise_leads": status_wise
        }

    def add_field_value(self, lead_id: str, field_id: str, value: str) -> LeadFieldValue:
        field_value = LeadFieldValue(lead_id=lead_id, field_id=field_id, value=value)
        self.db.add(field_value)
        self.db.commit()
        self.db.refresh(field_value)
        return field_value

    def get_field_values(self, lead_id: str) -> List[LeadFieldValue]:
        return self.db.query(LeadFieldValue).filter(LeadFieldValue.lead_id == lead_id).all()
