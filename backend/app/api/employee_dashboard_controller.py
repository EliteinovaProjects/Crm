from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_employee
from app.models.user import User
from app.schemas.dashboard_schemas import EmployeeDashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/employee/dashboard", tags=["Employee Dashboard"])


@router.get("/stats", response_model=EmployeeDashboardResponse)
def get_employee_dashboard_stats(
    current_user: User = Depends(get_current_employee),
    db: Session = Depends(get_db)
):
    """Get employee dashboard statistics"""
    dashboard_service = DashboardService(db)
    stats = dashboard_service.get_employee_dashboard_stats(current_user.id)
    return EmployeeDashboardResponse(**stats)
