from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.core.id_generator import generate_id
from app.services.excel_service import ExcelService

router = APIRouter(prefix="/toolbox/functionality", tags=["Toolbox Functionality"])


# Contacts Management
@router.post("/contacts")
def create_contact(
    name: str,
    phone_number: str,
    email: str = None,
    address: str = None,
    company: str = None,
    notes: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new contact"""
    from app.models.contact import Contact
    
    contact = Contact(
        id=generate_id("CNT", 6),
        name=name,
        phone_number=phone_number,
        email=email,
        address=address,
        company=company,
        notes=notes
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    return {
        "id": contact.id,
        "name": contact.name,
        "phone_number": contact.phone_number,
        "email": contact.email,
        "created_at": contact.created_at.isoformat()
    }


@router.get("/contacts")
def get_contacts(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all contacts"""
    from app.models.contact import Contact
    
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    
    return [
        {
            "id": contact.id,
            "name": contact.name,
            "phone_number": contact.phone_number,
            "email": contact.email,
            "company": contact.company,
            "created_at": contact.created_at.isoformat()
        }
        for contact in contacts
    ]


# Blacklist Management
@router.post("/blacklist")
def add_to_blacklist(
    phone_number: str,
    reason: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Add phone number to blacklist"""
    from app.models.blacklist import Blacklist
    
    blacklist = Blacklist(
        id=generate_id("BLK", 6),
        phone_number=phone_number,
        reason=reason,
        blocked_by=current_user.id
    )
    db.add(blacklist)
    db.commit()
    db.refresh(blacklist)
    
    return {
        "id": blacklist.id,
        "phone_number": blacklist.phone_number,
        "reason": blacklist.reason,
        "created_at": blacklist.created_at.isoformat()
    }


@router.get("/blacklist")
def get_blacklist(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get blacklist"""
    from app.models.blacklist import Blacklist
    
    blacklist = db.query(Blacklist).offset(skip).limit(limit).all()
    
    return [
        {
            "id": item.id,
            "phone_number": item.phone_number,
            "reason": item.reason,
            "blocked_by": item.blocked_by,
            "created_at": item.created_at.isoformat()
        }
        for item in blacklist
    ]


@router.delete("/blacklist/{item_id}")
def remove_from_blacklist(
    item_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Remove from blacklist"""
    from app.models.blacklist import Blacklist
    
    item = db.query(Blacklist).filter(Blacklist.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blacklist item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "Removed from blacklist successfully"}


# System Logs
@router.get("/system-logs")
def get_system_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get system logs"""
    from app.models.system_log import SystemLog
    
    logs = db.query(SystemLog).order_by(SystemLog.created_at.desc()).offset(skip).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "endpoint": log.endpoint,
            "method": log.method,
            "user_id": log.user_id,
            "ip_address": log.ip_address,
            "status_code": log.status_code,
            "processing_time": log.processing_time,
            "created_at": log.created_at.isoformat()
        }
        for log in logs
    ]


# Holidays Management
@router.post("/holidays")
def create_holiday(
    holiday_name: str,
    holiday_date: str,
    description: str = None,
    is_recurring: bool = False,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new holiday"""
    from app.models.holiday import Holiday
    from datetime import datetime
    
    holiday = Holiday(
        id=generate_id("HLD", 6),
        holiday_name=holiday_name,
        holiday_date=datetime.fromisoformat(holiday_date),
        description=description,
        is_recurring=is_recurring
    )
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    
    return {
        "id": holiday.id,
        "holiday_name": holiday.holiday_name,
        "holiday_date": holiday.holiday_date.isoformat(),
        "is_recurring": holiday.is_recurring,
        "created_at": holiday.created_at.isoformat()
    }


@router.get("/holidays")
def get_holidays(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all holidays"""
    from app.models.holiday import Holiday
    
    holidays = db.query(Holiday).offset(skip).limit(limit).all()
    
    return [
        {
            "id": holiday.id,
            "holiday_name": holiday.holiday_name,
            "holiday_date": holiday.holiday_date.isoformat(),
            "description": holiday.description,
            "is_recurring": holiday.is_recurring,
            "created_at": holiday.created_at.isoformat()
        }
        for holiday in holidays
    ]


# Break Reasons Management
@router.post("/break-reasons")
def create_break_reason(
    reason_name: str,
    description: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new break reason"""
    from app.models.break_reason import BreakReason
    
    reason = BreakReason(
        id=generate_id("BRR", 6),
        reason_name=reason_name,
        description=description
    )
    db.add(reason)
    db.commit()
    db.refresh(reason)
    
    return {
        "id": reason.id,
        "reason_name": reason.reason_name,
        "description": reason.description,
        "created_at": reason.created_at.isoformat()
    }


@router.get("/break-reasons")
def get_break_reasons(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all break reasons"""
    from app.models.break_reason import BreakReason
    
    reasons = db.query(BreakReason).offset(skip).limit(limit).all()
    
    return [
        {
            "id": reason.id,
            "reason_name": reason.reason_name,
            "description": reason.description,
            "is_active": reason.is_active,
            "created_at": reason.created_at.isoformat()
        }
        for reason in reasons
    ]


# Disposition Management
@router.post("/dispositions")
def create_disposition(
    disposition_name: str,
    description: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new disposition"""
    from app.models.disposition import Disposition
    
    disposition = Disposition(
        id=generate_id("DSP", 6),
        disposition_name=disposition_name,
        description=description
    )
    db.add(disposition)
    db.commit()
    db.refresh(disposition)
    
    return {
        "id": disposition.id,
        "disposition_name": disposition.disposition_name,
        "description": disposition.description,
        "created_at": disposition.created_at.isoformat()
    }


@router.get("/dispositions")
def get_dispositions(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all dispositions"""
    from app.models.disposition import Disposition
    
    dispositions = db.query(Disposition).offset(skip).limit(limit).all()
    
    return [
        {
            "id": disposition.id,
            "disposition_name": disposition.disposition_name,
            "description": disposition.description,
            "is_active": disposition.is_active,
            "created_at": disposition.created_at.isoformat()
        }
        for disposition in dispositions
    ]


# API Integration
@router.post("/api-integrations")
def create_api_integration(
    integration_name: str,
    api_key: str,
    api_secret: str,
    endpoint_url: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new API integration"""
    from app.models.api_integration import APIIntegration
    
    integration = APIIntegration(
        id=generate_id("API", 6),
        integration_name=integration_name,
        api_key=api_key,
        api_secret=api_secret,
        endpoint_url=endpoint_url
    )
    db.add(integration)
    db.commit()
    db.refresh(integration)
    
    return {
        "id": integration.id,
        "integration_name": integration.integration_name,
        "endpoint_url": integration.endpoint_url,
        "is_active": integration.is_active,
        "created_at": integration.created_at.isoformat()
    }


@router.get("/api-integrations")
def get_api_integrations(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all API integrations"""
    from app.models.api_integration import APIIntegration
    
    integrations = db.query(APIIntegration).offset(skip).limit(limit).all()
    
    return [
        {
            "id": integration.id,
            "integration_name": integration.integration_name,
            "endpoint_url": integration.endpoint_url,
            "is_active": integration.is_active,
            "created_at": integration.created_at.isoformat()
        }
        for integration in integrations
    ]


# Export Functionality
@router.post("/export/leads")
async def export_leads(
    start_date: str = None,
    end_date: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export leads to Excel"""
    from app.models.lead import Lead
    from datetime import datetime
    
    query = db.query(Lead).filter(Lead.is_deleted == False)
    
    if start_date:
        query = query.filter(Lead.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Lead.created_at <= datetime.fromisoformat(end_date))
    
    leads = query.all()
    
    data = [
        {
            "ID": lead.id,
            "Name": lead.name,
            "Mobile": lead.mobile_number,
            "Email": lead.email,
            "Account": lead.account,
            "Created At": lead.created_at.isoformat()
        }
        for lead in leads
    ]
    
    excel_service = ExcelService()
    excel_data = excel_service.generate_export_file(data, "leads_export")
    
    return StreamingResponse(
        iter([excel_data]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=leads_export.xlsx"}
    )


# Configuration (Text to Speech, etc.)
@router.post("/config/tts")
def update_tts_config(
    enabled: bool,
    provider: str = None,
    api_key: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update Text-to-Speech configuration"""
    # This would typically store configuration in a settings table
    return {
        "message": "TTS configuration updated successfully",
        "enabled": enabled,
        "provider": provider
    }


@router.get("/config/tts")
def get_tts_config(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get Text-to-Speech configuration"""
    # This would typically retrieve configuration from a settings table
    return {
        "enabled": False,
        "provider": None,
        "configured": False
    }
