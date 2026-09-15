from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.sms_template_schemas import SMSTemplateCreate, SMSTemplateUpdate, SMSTemplateResponse
from app.services.sms_service import SMSService

router = APIRouter(prefix="/sms-templates", tags=["SMS Templates"])


@router.post("/", response_model=SMSTemplateResponse)
def create_template(
    template_data: SMSTemplateCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new SMS template"""
    sms_service = SMSService(db)
    
    try:
        template = sms_service.create_template(template_data.dict())
        return SMSTemplateResponse.from_orm(template)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[SMSTemplateResponse])
def get_templates(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all SMS templates"""
    sms_service = SMSService(db)
    templates = sms_service.get_all_templates(skip, limit)
    return [SMSTemplateResponse.from_orm(template) for template in templates]


@router.get("/{template_id}", response_model=SMSTemplateResponse)
def get_template(
    template_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get template by ID"""
    sms_service = SMSService(db)
    template = sms_service.get_template(template_id)
    
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    return SMSTemplateResponse.from_orm(template)


@router.put("/{template_id}", response_model=SMSTemplateResponse)
def update_template(
    template_id: str,
    template_data: SMSTemplateUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update template"""
    sms_service = SMSService(db)
    
    try:
        template = sms_service.update_template(template_id, template_data.dict(exclude_unset=True))
        return SMSTemplateResponse.from_orm(template)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{template_id}")
def delete_template(
    template_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete template"""
    sms_service = SMSService(db)
    
    try:
        sms_service.delete_template(template_id)
        return {"message": "Template deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/send")
def send_sms(
    phone_number: str,
    template_id: str,
    variables: dict = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Send SMS using template"""
    sms_service = SMSService(db)
    
    try:
        result = sms_service.send_sms(phone_number, template_id, variables)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
