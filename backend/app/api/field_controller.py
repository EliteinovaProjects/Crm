from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.field_schemas import (
    LeadFieldCreate, LeadFieldUpdate, LeadFieldResponse,
    LeadFieldValueResponse
)
from app.services.field_mapping_service import FieldMappingService

router = APIRouter(prefix="/fields", tags=["Fields"])


@router.post("/", response_model=LeadFieldResponse)
def create_field(
    field_data: LeadFieldCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new custom field"""
    field_service = FieldMappingService(db)
    
    try:
        field = field_service.create_field(field_data.dict())
        return LeadFieldResponse.from_orm(field)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[LeadFieldResponse])
def get_fields(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all custom fields"""
    field_service = FieldMappingService(db)
    fields = field_service.get_all_fields(skip, limit)
    return [LeadFieldResponse.from_orm(field) for field in fields]


@router.get("/{field_id}", response_model=LeadFieldResponse)
def get_field(
    field_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get field by ID"""
    field_service = FieldMappingService(db)
    field = field_service.get_field(field_id)
    
    if not field:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field not found"
        )
    
    return LeadFieldResponse.from_orm(field)


@router.put("/{field_id}", response_model=LeadFieldResponse)
def update_field(
    field_id: str,
    field_data: LeadFieldUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update field"""
    field_service = FieldMappingService(db)
    
    try:
        field = field_service.update_field(field_id, field_data.dict(exclude_unset=True))
        return LeadFieldResponse.from_orm(field)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{field_id}")
def delete_field(
    field_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete field"""
    field_service = FieldMappingService(db)
    
    try:
        field_service.delete_field(field_id)
        return {"message": "Field deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{lead_id}/values/{field_id}", response_model=LeadFieldValueResponse)
def add_field_value(
    lead_id: str,
    field_id: str,
    value: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add field value for a lead"""
    field_service = FieldMappingService(db)
    
    try:
        field_value = field_service.add_field_value(lead_id, field_id, value)
        return LeadFieldValueResponse.from_orm(field_value)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{lead_id}/values", response_model=List[LeadFieldValueResponse])
def get_lead_field_values(
    lead_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all field values for a lead"""
    field_service = FieldMappingService(db)
    field_values = field_service.get_field_values_for_lead(lead_id)
    return [LeadFieldValueResponse.from_orm(fv) for fv in field_values]
