from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.middleware.auth_middleware import get_current_admin
from app.models.user import User
from app.schemas.category_schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from app.core.id_generator import generate_id

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new lead category"""
    from app.models.category import Category
    
    category = Category(
        id=generate_id("CAT", 6),
        **category_data.dict()
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.from_orm(category)


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all lead categories"""
    from app.models.category import Category
    
    categories = db.query(Category).offset(skip).limit(limit).all()
    return [CategoryResponse.from_orm(category) for category in categories]


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get category by ID"""
    from app.models.category import Category
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return CategoryResponse.from_orm(category)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update category"""
    from app.models.category import Category
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(category, key, value)
    
    db.commit()
    db.refresh(category)
    
    return CategoryResponse.from_orm(category)


@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete category"""
    from app.models.category import Category
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}
