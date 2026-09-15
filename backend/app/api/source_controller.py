from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.source_schemas import SourceCreate, SourceUpdate, SourceResponse
from app.core.id_generator import generate_id

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.post("/", response_model=SourceResponse)
def create_source(
    source_data: SourceCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new lead source"""
    from app.models.source import Source
    
    source = Source(
        id=generate_id("SRC", 6),
        **source_data.dict()
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    
    return SourceResponse.from_orm(source)


@router.get("/", response_model=List[SourceResponse])
def get_sources(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all lead sources"""
    from app.models.source import Source
    
    sources = db.query(Source).offset(skip).limit(limit).all()
    return [SourceResponse.from_orm(source) for source in sources]


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(
    source_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get source by ID"""
    from app.models.source import Source
    
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    
    return SourceResponse.from_orm(source)


@router.put("/{source_id}", response_model=SourceResponse)
def update_source(
    source_id: str,
    source_data: SourceUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update source"""
    from app.models.source import Source
    
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    
    for key, value in source_data.dict(exclude_unset=True).items():
        setattr(source, key, value)
    
    db.commit()
    db.refresh(source)
    
    return SourceResponse.from_orm(source)


@router.delete("/{source_id}")
def delete_source(
    source_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete source"""
    from app.models.source import Source
    
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found"
        )
    
    db.delete(source)
    db.commit()
    
    return {"message": "Source deleted successfully"}
