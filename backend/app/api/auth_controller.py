from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_user, get_current_admin
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserCreate, UserUpdate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return access token"""
    auth_service = AuthService(db)
    result = auth_service.login(login_data.username, login_data.password)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if login_data.portal and result["user"]["role"] not in (["employee"] if login_data.portal == "employee" else ["admin", "sub_admin"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "wrong_portal",
                "role": result["user"]["role"],
                "message": f"This account is registered as an {result['user']['role'].replace('_', ' ').title()}. Please use the correct login.",
            },
        )

    return result


@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Register a new user (Admin only)"""
    auth_service = AuthService(db)
    
    try:
        user = auth_service.register_user(user_data.dict(), current_user)
        return UserResponse.from_orm(user)
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse.from_orm(current_user)


@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    auth_service = AuthService(db)
    
    try:
        updated_user = auth_service.update_user(current_user.id, user_data.dict(exclude_unset=True), current_user)
        return UserResponse.from_orm(updated_user)
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all users (Admin only)"""
    auth_service = AuthService(db)
    
    try:
        users = auth_service.get_all_users(current_user, skip, limit)
        return users
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update user by ID (Admin only)"""
    auth_service = AuthService(db)
    
    try:
        updated_user = auth_service.update_user(user_id, user_data.dict(exclude_unset=True), current_user)
        return UserResponse.from_orm(updated_user)
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete user by ID (Admin only)"""
    auth_service = AuthService(db)
    
    try:
        auth_service.delete_user(user_id, current_user)
        return {"message": "User deleted successfully"}
    except (ValueError, PermissionError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
