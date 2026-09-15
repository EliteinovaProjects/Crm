from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.campaign_schemas import (
    CampaignCreate, CampaignUpdate, CampaignResponse,
    CampaignBaseCreate, CampaignBaseResponse, CampaignField
)
from app.services.campaign_service import CampaignService

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("/", response_model=CampaignResponse)
def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new campaign"""
    campaign_service = CampaignService(db)
    
    try:
        campaign = campaign_service.create_campaign(campaign_data.dict())
        return CampaignResponse.from_orm(campaign)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all campaigns"""
    campaign_service = CampaignService(db)
    campaigns = campaign_service.get_all_campaigns(skip, limit, active_only)
    return [CampaignResponse.from_orm(campaign) for campaign in campaigns]


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get campaign by ID"""
    campaign_service = CampaignService(db)
    campaign = campaign_service.get_campaign(campaign_id)
    
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return CampaignResponse.from_orm(campaign)


@router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update campaign"""
    campaign_service = CampaignService(db)
    
    try:
        campaign = campaign_service.update_campaign(campaign_id, campaign_data.dict(exclude_unset=True))
        return CampaignResponse.from_orm(campaign)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{campaign_id}")
def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete campaign"""
    campaign_service = CampaignService(db)
    
    try:
        campaign_service.delete_campaign(campaign_id)
        return {"message": "Campaign deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{campaign_id}/activate")
def activate_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Activate campaign"""
    campaign_service = CampaignService(db)
    
    try:
        campaign = campaign_service.activate_campaign(campaign_id)
        return {"message": "Campaign activated successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{campaign_id}/deactivate")
def deactivate_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Deactivate campaign"""
    campaign_service = CampaignService(db)
    
    try:
        campaign = campaign_service.deactivate_campaign(campaign_id)
        return {"message": "Campaign deactivated successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# Campaign Base (Contacts)
@router.post("/{campaign_id}/base", response_model=List[CampaignBaseResponse])
def add_campaign_base(
    campaign_id: str,
    base_data: CampaignBaseCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add contacts to campaign base"""
    campaign_service = CampaignService(db)
    
    try:
        bases = campaign_service.add_campaign_base(campaign_id, [contact.dict() for contact in base_data.contacts])
        return [CampaignBaseResponse.from_orm(base) for base in bases]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{campaign_id}/base", response_model=List[CampaignBaseResponse])
def get_campaign_base(
    campaign_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get campaign base contacts"""
    campaign_service = CampaignService(db)
    bases = campaign_service.get_campaign_bases(campaign_id, skip, limit)
    return [CampaignBaseResponse.from_orm(base) for base in bases]


@router.get("/{campaign_id}/base/pending", response_model=List[CampaignBaseResponse])
def get_pending_calls(
    campaign_id: str,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get pending calls for campaign"""
    campaign_service = CampaignService(db)
    bases = campaign_service.get_pending_calls(campaign_id, limit)
    return [CampaignBaseResponse.from_orm(base) for base in bases]


@router.put("/base/{base_id}/status")
def update_call_status(
    base_id: str,
    status: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update call status for campaign base contact"""
    campaign_service = CampaignService(db)
    
    try:
        base = campaign_service.update_call_status(base_id, status)
        return CampaignBaseResponse.from_orm(base)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/base/{base_id}")
def delete_campaign_base(
    base_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete campaign base contact"""
    campaign_service = CampaignService(db)
    
    try:
        campaign_service.delete_campaign_base(base_id)
        return {"message": "Campaign base contact deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


# Campaign Fields
@router.post("/{campaign_id}/fields")
def add_campaign_field(
    campaign_id: str,
    field_data: CampaignField,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add custom field to campaign"""
    # This would typically store campaign-specific field configurations
    return {
        "message": "Field added to campaign successfully",
        "campaign_id": campaign_id,
        "field_name": field_data.field_name
    }
