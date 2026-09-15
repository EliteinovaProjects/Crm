from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.status_schemas import StatusCreate, StatusUpdate, StatusResponse
from app.core.id_generator import generate_id

router = APIRouter(prefix="/statuses", tags=["Statuses"])


@router.post("/", response_model=StatusResponse)
def create_status(
    status_data: StatusCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new lead status"""
    from app.models.status import Status
    
    status = Status(
        id=generate_id("STS", 6),
        **status_data.dict()
    )
    db.add(status)
    db.commit()
    db.refresh(status)
    
    return StatusResponse.from_orm(status)


@router.get("/", response_model=List[StatusResponse])
def get_statuses(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all lead statuses"""
    from app.models.status import Status
    
    statuses = db.query(Status).offset(skip).limit(limit).all()
    return [StatusResponse.from_orm(status) for status in statuses]


@router.get("/{status_id}", response_model=StatusResponse)
def get_status(
    status_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get status by ID"""
    from app.models.status import Status
    
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found"
        )
    
    return StatusResponse.from_orm(status)


@router.put("/{status_id}", response_model=StatusResponse)
def update_status(
    status_id: str,
    status_data: StatusUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update status"""
    from app.models.status import Status
    
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found"
        )
    
    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(status, key, value)
    
    db.commit()
    db.refresh(status)
    
    return StatusResponse.from_orm(status)


@router.delete("/{status_id}")
def delete_status(
    status_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete status"""
    from app.models.status import Status
    
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status not found"
        )
    
    db.delete(status)
    db.commit()
    
    return {"message": "Status deleted successfully"}
