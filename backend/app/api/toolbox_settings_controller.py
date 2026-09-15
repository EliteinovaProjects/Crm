from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.core.id_generator import generate_id

router = APIRouter(prefix="/toolbox/settings", tags=["Toolbox Settings"])


# IVR Flow Designer
@router.post("/ivr-flows")
def create_ivr_flow(
    flow_name: str,
    flow_config: dict,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new IVR flow"""
    from app.models.ivr_flow import IVRFlow
    
    import json
    flow = IVRFlow(
        id=generate_id("IVR", 6),
        flow_name=flow_name,
        flow_config=json.dumps(flow_config)
    )
    db.add(flow)
    db.commit()
    db.refresh(flow)
    
    return {
        "id": flow.id,
        "flow_name": flow.flow_name,
        "flow_config": json.loads(flow.flow_config),
        "created_at": flow.created_at.isoformat()
    }


@router.get("/ivr-flows")
def get_ivr_flows(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all IVR flows"""
    from app.models.ivr_flow import IVRFlow
    
    flows = db.query(IVRFlow).offset(skip).limit(limit).all()
    
    import json
    return [
        {
            "id": flow.id,
            "flow_name": flow.flow_name,
            "flow_config": json.loads(flow.flow_config),
            "created_at": flow.created_at.isoformat(),
            "updated_at": flow.updated_at.isoformat()
        }
        for flow in flows
    ]


@router.get("/ivr-flows/{flow_id}")
def get_ivr_flow(
    flow_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get IVR flow by ID"""
    from app.models.ivr_flow import IVRFlow
    
    flow = db.query(IVRFlow).filter(IVRFlow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IVR flow not found"
        )
    
    import json
    return {
        "id": flow.id,
        "flow_name": flow.flow_name,
        "flow_config": json.loads(flow.flow_config),
        "created_at": flow.created_at.isoformat(),
        "updated_at": flow.updated_at.isoformat()
    }


@router.put("/ivr-flows/{flow_id}")
def update_ivr_flow(
    flow_id: str,
    flow_name: str = None,
    flow_config: dict = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update IVR flow"""
    from app.models.ivr_flow import IVRFlow
    
    flow = db.query(IVRFlow).filter(IVRFlow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IVR flow not found"
        )
    
    if flow_name:
        flow.flow_name = flow_name
    if flow_config:
        import json
        flow.flow_config = json.dumps(flow_config)
    
    db.commit()
    db.refresh(flow)
    
    import json
    return {
        "id": flow.id,
        "flow_name": flow.flow_name,
        "flow_config": json.loads(flow.flow_config),
        "updated_at": flow.updated_at.isoformat()
    }


@router.delete("/ivr-flows/{flow_id}")
def delete_ivr_flow(
    flow_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete IVR flow"""
    from app.models.ivr_flow import IVRFlow
    
    flow = db.query(IVRFlow).filter(IVRFlow.id == flow_id).first()
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="IVR flow not found"
        )
    
    db.delete(flow)
    db.commit()
    
    return {"message": "IVR flow deleted successfully"}


# Sub-Admin Management
@router.post("/sub-admins")
def create_sub_admin(
    email: str,
    username: str,
    password: str,
    full_name: str = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new sub-admin (Admin only)"""
    from app.models.user import User, UserRole
    from app.core.security import get_password_hash
    
    # Check if current user is admin
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create sub-admins"
        )
    
    sub_admin = User(
        id=generate_id("USR", 6),
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        role=UserRole.SUB_ADMIN
    )
    db.add(sub_admin)
    db.commit()
    db.refresh(sub_admin)
    
    return {
        "id": sub_admin.id,
        "email": sub_admin.email,
        "username": sub_admin.username,
        "full_name": sub_admin.full_name,
        "role": sub_admin.role.value,
        "created_at": sub_admin.created_at.isoformat()
    }


@router.get("/sub-admins")
def get_sub_admins(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all sub-admins"""
    from app.models.user import User, UserRole
    
    sub_admins = db.query(User).filter(User.role == UserRole.SUB_ADMIN).offset(skip).limit(limit).all()
    
    return [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        }
        for user in sub_admins
    ]
