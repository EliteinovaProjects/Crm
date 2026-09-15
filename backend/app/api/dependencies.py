from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user, get_current_admin, get_current_employee
from app.models.user import User


def get_db_dependency():
    return Depends(get_db)


def get_current_user_dependency():
    return Depends(get_current_user)


def get_current_admin_dependency():
    return Depends(get_current_admin)


def get_current_employee_dependency():
    return Depends(get_current_employee)
