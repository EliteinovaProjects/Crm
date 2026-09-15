from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.lead_request import (
    LeadCreate, LeadUpdate, LeadBulkUpdate, LeadAssign,
    LeadImportRequest, LeadExportRequest
)
from app.schemas.lead_response import LeadDetailResponse, LeadListResponse, LeadStatsResponse
from app.services.lead_service import LeadService

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.post("/", response_model=LeadDetailResponse)
def create_lead(
    lead_data: LeadCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new lead"""
    lead_service = LeadService(db)
    
    try:
        lead = lead_service.create_lead(lead_data.dict())
        return LeadDetailResponse.from_orm(lead)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=LeadListResponse)
def get_leads(
    skip: int = 0,
    limit: int = 100,
    agent_id: Optional[str] = None,
    status_id: Optional[str] = None,
    source_id: Optional[str] = None,
    category_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get leads with optional filters"""
    lead_service = LeadService(db)
    
    filters = {}
    if agent_id:
        filters["agent_id"] = agent_id
    if status_id:
        filters["status_id"] = status_id
    if source_id:
        filters["source_id"] = source_id
    if category_id:
        filters["category_id"] = category_id
    
    # Employees can only see their own leads
    if current_user.role.value == "employee":
        filters["agent_id"] = current_user.id
    
    leads = lead_service.get_leads(skip, limit, filters)
    total = len(leads)
    
    return LeadListResponse(
        leads=[LeadDetailResponse.from_orm(lead) for lead in leads],
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_lead(
    lead_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get lead by ID"""
    lead_service = LeadService(db)
    lead = lead_service.get_lead(lead_id)
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Employees can only see their own leads
    if current_user.role.value == "employee" and lead.assigned_agent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this lead"
        )
    
    return LeadDetailResponse.from_orm(lead)


@router.put("/{lead_id}", response_model=LeadDetailResponse)
def update_lead(
    lead_id: str,
    lead_data: LeadUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update lead"""
    lead_service = LeadService(db)
    
    try:
        lead = lead_service.update_lead(lead_id, lead_data.dict(exclude_unset=True))
        return LeadDetailResponse.from_orm(lead)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{lead_id}")
def delete_lead(
    lead_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Soft delete lead"""
    lead_service = LeadService(db)
    
    try:
        lead_service.delete_lead(lead_id)
        return {"message": "Lead deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{lead_id}/restore")
def restore_lead(
    lead_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Restore deleted lead"""
    lead_service = LeadService(db)
    
    try:
        lead_service.restore_lead(lead_id)
        return {"message": "Lead restored successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/assign")
def assign_leads(
    assign_data: LeadAssign,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Bulk assign leads to agents"""
    lead_service = LeadService(db)
    
    try:
        leads = lead_service.bulk_assign_leads(assign_data.lead_ids, assign_data.agent_ids)
        return {
            "message": f"Successfully assigned {len(leads)} leads",
            "assigned_count": len(leads)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/bulk-update")
def bulk_update_leads(
    bulk_update_data: LeadBulkUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Bulk update leads"""
    lead_service = LeadService(db)
    
    try:
        leads = lead_service.bulk_update_leads(
            bulk_update_data.lead_ids,
            bulk_update_data.update_type,
            bulk_update_data.update_value
        )
        return {
            "message": f"Successfully updated {len(leads)} leads",
            "updated_count": len(leads)
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/import")
async def import_leads(
    file: UploadFile = File(...),
    agent_id: Optional[str] = None,
    source_id: Optional[str] = None,
    status_id: Optional[str] = None,
    category_id: Optional[str] = None,
    follow_up_date: Optional[str] = None,
    restore_deleted: bool = False,
    reassign_existing: bool = False,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Import leads from Excel file"""
    lead_service = LeadService(db)
    
    try:
        file_content = await file.read()
        
        import_options = {
            "agent_id": agent_id,
            "source_id": source_id,
            "status_id": status_id,
            "category_id": category_id,
            "follow_up_date": follow_up_date,
            "restore_deleted": restore_deleted,
            "reassign_existing": reassign_existing
        }
        
        result = lead_service.import_leads_from_excel(file_content, import_options)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/export")
async def export_leads(
    export_data: LeadExportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export leads to Excel"""
    lead_service = LeadService(db)
    
    try:
        excel_data = lead_service.export_leads_to_excel(export_data.dict(exclude_unset=True))
        
        return StreamingResponse(
            iter([excel_data]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=leads_export.xlsx"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/sample/download")
async def download_sample_sheet():
    """Download sample Excel sheet for lead import"""
    lead_service = LeadService(None)  # We don't need db for sample sheet
    
    try:
        sample_data = lead_service.get_sample_excel_template()
        
        return StreamingResponse(
            iter([sample_data]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=sample_leads.xlsx"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/stats", response_model=LeadStatsResponse)
def get_lead_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get lead statistics"""
    lead_service = LeadService(db)
    stats = lead_service.get_lead_stats()
    return LeadStatsResponse(**stats)
