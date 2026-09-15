from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.dashboard_schemas import DashboardStatsResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/admin/dashboard", tags=["Admin Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_admin_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    dashboard_service = DashboardService(db)
    stats = dashboard_service.get_admin_dashboard_stats()
    return DashboardStatsResponse(**stats)
