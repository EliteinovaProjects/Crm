from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.reminder_schemas import (
    ReminderCreate, ReminderUpdate, ReminderResponse, ReminderListResponse
)
from app.services.reminder_service import ReminderService

router = APIRouter(prefix="/reminders", tags=["Reminders"])


@router.post("/", response_model=ReminderResponse)
def create_reminder(
    reminder_data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new reminder"""
    reminder_service = ReminderService(db)
    
    try:
        reminder = reminder_service.create_reminder(current_user.id, reminder_data.dict())
        return ReminderResponse.from_orm(reminder)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[ReminderResponse])
def get_reminders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's reminders"""
    reminder_service = ReminderService(db)
    reminders = reminder_service.get_user_reminders(current_user.id, skip, limit)
    return [ReminderResponse.from_orm(reminder) for reminder in reminders]


@router.get("/upcoming", response_model=List[ReminderResponse])
def get_upcoming_reminders(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get upcoming reminders"""
    reminder_service = ReminderService(db)
    reminders = reminder_service.get_upcoming_reminders(current_user.id, limit)
    return [ReminderResponse.from_orm(reminder) for reminder in reminders]


@router.get("/history", response_model=List[ReminderResponse])
def get_reminder_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get reminder history"""
    reminder_service = ReminderService(db)
    reminders = reminder_service.get_reminder_history(current_user.id, skip, limit)
    return [ReminderResponse.from_orm(reminder) for reminder in reminders]


@router.get("/summary", response_model=ReminderListResponse)
def get_reminders_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get reminders summary"""
    reminder_service = ReminderService(db)
    summary = reminder_service.get_reminders_summary(current_user.id)
    return ReminderListResponse(**summary)


@router.get("/{reminder_id}", response_model=ReminderResponse)
def get_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get reminder by ID"""
    reminder_service = ReminderService(db)
    reminder = reminder_service.get_reminder(reminder_id)
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Users can only see their own reminders
    if reminder.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this reminder"
        )
    
    return ReminderResponse.from_orm(reminder)


@router.put("/{reminder_id}", response_model=ReminderResponse)
def update_reminder(
    reminder_id: str,
    reminder_data: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update reminder"""
    reminder_service = ReminderService(db)
    
    try:
        reminder = reminder_service.update_reminder(reminder_id, reminder_data.dict(exclude_unset=True))
        
        # Check ownership
        if reminder.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this reminder"
            )
        
        return ReminderResponse.from_orm(reminder)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/{reminder_id}/complete")
def complete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark reminder as completed"""
    reminder_service = ReminderService(db)
    
    try:
        reminder = reminder_service.complete_reminder(reminder_id)
        
        # Check ownership
        if reminder.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to complete this reminder"
            )
        
        return ReminderResponse.from_orm(reminder)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete reminder"""
    reminder_service = ReminderService(db)
    
    try:
        reminder = reminder_service.get_reminder(reminder_id)
        
        # Check ownership
        if reminder.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this reminder"
            )
        
        reminder_service.delete_reminder(reminder_id)
        return {"message": "Reminder deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
