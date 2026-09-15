from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.core.security import create_access_token, verify_password
from app.core.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.authenticate(username, password)
        if not user or not self.user_repository.is_active(user):
            return None
        return user

    def create_access_token(self, user: User) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": user.id, "role": user.role.value}
        return create_access_token(token_data, access_token_expires)

    def login(self, username: str, password: str) -> Optional[dict]:
        user = self.authenticate_user(username, password)
        if not user:
            return None
        
        access_token = self.create_access_token(user)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role.value,
                "is_active": user.is_active,
                "phone": user.phone,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
        }

    def register_user(self, user_data: dict, current_user: User) -> User:
        # Only admin and sub-admin can create users
        if current_user.role not in [UserRole.ADMIN, UserRole.SUB_ADMIN]:
            raise PermissionError("Only admins can create users")
        
        # Sub-admins can only create employees
        if current_user.role == UserRole.SUB_ADMIN and user_data.get("role") != UserRole.EMPLOYEE:
            raise PermissionError("Sub-admins can only create employees")
        
        return self.user_repository.create(user_data)

    def get_current_user_info(self, user_id: str) -> Optional[dict]:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "phone": user.phone,
            "created_at": user.created_at.isoformat()
        }

    def update_user(self, user_id: str, user_data: dict, current_user: User) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Check permissions
        if current_user.role == UserRole.EMPLOYEE and current_user.id != user_id:
            raise PermissionError("Employees can only update their own profile")
        
        if current_user.role == UserRole.SUB_ADMIN and user.role != UserRole.EMPLOYEE:
            raise PermissionError("Sub-admins can only update employees")
        
        return self.user_repository.update(user, user_data)

    def delete_user(self, user_id: str, current_user: User) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Only admins can delete users
        if current_user.role != UserRole.ADMIN:
            raise PermissionError("Only admins can delete users")
        
        return self.user_repository.delete(user)

    def get_all_users(self, current_user: User, skip: int = 0, limit: int = 100) -> list:
        if current_user.role not in [UserRole.ADMIN, UserRole.SUB_ADMIN]:
            raise PermissionError("Only admins can view all users")
        
        users = self.user_repository.get_all(skip, limit)
        return [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "role": user.role.value,
                "is_active": user.is_active,
                "phone": user.phone,
                "created_at": user.created_at.isoformat()
            }
            for user in users
        ]
