from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.campaign import Campaign
from app.models.campaign_base import CampaignBase
from app.repositories.campaign_repository import CampaignRepository, CampaignBaseRepository
from app.core.id_generator import generate_campaign_id, generate_id


class CampaignService:
    def __init__(self, db: Session):
        self.db = db
        self.campaign_repository = CampaignRepository(db)
        self.campaign_base_repository = CampaignBaseRepository(db)

    def create_campaign(self, campaign_data: dict) -> Campaign:
        campaign_data["id"] = generate_campaign_id()
        return self.campaign_repository.create(campaign_data)

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        return self.campaign_repository.get_by_id(campaign_id)

    def get_all_campaigns(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Campaign]:
        return self.campaign_repository.get_all(skip, limit, active_only)

    def update_campaign(self, campaign_id: str, campaign_data: dict) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        return self.campaign_repository.update(campaign, campaign_data)

    def delete_campaign(self, campaign_id: str) -> bool:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        return self.campaign_repository.delete(campaign)

    def activate_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        return self.campaign_repository.activate(campaign)

    def deactivate_campaign(self, campaign_id: str) -> Campaign:
        campaign = self.get_campaign(campaign_id)
        if not campaign:
            raise ValueError("Campaign not found")
        return self.campaign_repository.deactivate(campaign)

    def add_campaign_base(self, campaign_id: str, contacts_data: List[dict]) -> List[CampaignBase]:
        bases = []
        for contact_data in contacts_data:
            contact_data["id"] = generate_id("CB", 6)
            contact_data["campaign_id"] = campaign_id
            base = self.campaign_base_repository.create(contact_data)
            bases.append(base)
        return bases

    def get_campaign_base(self, base_id: str) -> Optional[CampaignBase]:
        return self.campaign_base_repository.get_by_id(base_id)

    def get_campaign_bases(self, campaign_id: str, skip: int = 0, limit: int = 100) -> List[CampaignBase]:
        return self.campaign_base_repository.get_by_campaign(campaign_id, skip, limit)

    def get_pending_calls(self, campaign_id: str, limit: int = 100) -> List[CampaignBase]:
        return self.campaign_base_repository.get_pending_calls(campaign_id, limit)

    def update_call_status(self, base_id: str, status: str) -> CampaignBase:
        base = self.get_campaign_base(base_id)
        if not base:
            raise ValueError("Campaign base not found")
        return self.campaign_base_repository.update_call_status(base, status)

    def delete_campaign_base(self, base_id: str) -> bool:
        base = self.get_campaign_base(base_id)
        if not base:
            raise ValueError("Campaign base not found")
        return self.campaign_base_repository.delete(base)

    def get_active_campaigns_for_dialer(self) -> List[Campaign]:
        return self.campaign_repository.get_active_campaigns()

    def get_next_contact_to_call(self, campaign_id: str) -> Optional[CampaignBase]:
        pending_contacts = self.get_pending_calls(campaign_id, limit=1)
        return pending_contacts[0] if pending_contacts else None
