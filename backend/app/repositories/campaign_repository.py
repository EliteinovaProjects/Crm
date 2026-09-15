from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from app.models.campaign import Campaign
from app.models.campaign_base import CampaignBase


class CampaignRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, campaign_id: str) -> Optional[Campaign]:
        return self.db.query(Campaign).filter(Campaign.id == campaign_id).first()

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Campaign]:
        query = self.db.query(Campaign)
        if active_only:
            query = query.filter(Campaign.is_active == True)
        return query.offset(skip).limit(limit).all()

    def get_active_campaigns(self) -> List[Campaign]:
        return self.db.query(Campaign).filter(
            Campaign.is_active == True,
            Campaign.scheduled_at <= datetime.utcnow(),
            Campaign.closure_at >= datetime.utcnow()
        ).all()

    def create(self, campaign_data: dict) -> Campaign:
        db_campaign = Campaign(**campaign_data)
        self.db.add(db_campaign)
        self.db.commit()
        self.db.refresh(db_campaign)
        return db_campaign

    def update(self, campaign: Campaign, campaign_data: dict) -> Campaign:
        for key, value in campaign_data.items():
            if hasattr(campaign, key) and value is not None:
                setattr(campaign, key, value)
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def delete(self, campaign: Campaign) -> bool:
        self.db.delete(campaign)
        self.db.commit()
        return True

    def activate(self, campaign: Campaign) -> Campaign:
        campaign.is_active = True
        self.db.commit()
        self.db.refresh(campaign)
        return campaign

    def deactivate(self, campaign: Campaign) -> Campaign:
        campaign.is_active = False
        self.db.commit()
        self.db.refresh(campaign)
        return campaign


class CampaignBaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, base_id: str) -> Optional[CampaignBase]:
        return self.db.query(CampaignBase).filter(CampaignBase.id == base_id).first()

    def get_by_campaign(self, campaign_id: str, skip: int = 0, limit: int = 100) -> List[CampaignBase]:
        return self.db.query(CampaignBase).filter(
            CampaignBase.campaign_id == campaign_id
        ).offset(skip).limit(limit).all()

    def get_pending_calls(self, campaign_id: str, limit: int = 100) -> List[CampaignBase]:
        return self.db.query(CampaignBase).filter(
            CampaignBase.campaign_id == campaign_id,
            CampaignBase.call_status == "pending",
            CampaignBase.is_active == True
        ).limit(limit).all()

    def create(self, base_data: dict) -> CampaignBase:
        db_base = CampaignBase(**base_data)
        self.db.add(db_base)
        self.db.commit()
        self.db.refresh(db_base)
        return db_base

    def bulk_create(self, contacts_data: List[dict]) -> List[CampaignBase]:
        db_bases = [CampaignBase(**contact_data) for contact_data in contacts_data]
        self.db.add_all(db_bases)
        self.db.commit()
        for base in db_bases:
            self.db.refresh(base)
        return db_bases

    def update(self, base: CampaignBase, base_data: dict) -> CampaignBase:
        for key, value in base_data.items():
            if hasattr(base, key) and value is not None:
                setattr(base, key, value)
        self.db.commit()
        self.db.refresh(base)
        return base

    def update_call_status(self, base: CampaignBase, status: str) -> CampaignBase:
        base.call_status = status
        base.call_attempts += 1
        if status in ["called", "completed"]:
            base.last_called_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(base)
        return base

    def delete(self, base: CampaignBase) -> bool:
        self.db.delete(base)
        self.db.commit()
        return True
