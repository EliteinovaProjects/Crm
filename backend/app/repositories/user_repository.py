from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User, UserRole
from app.core.security import get_password_hash, verify_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

    def create(self, user_data: dict) -> User:
        hashed_password = get_password_hash(user_data.pop("password"))
        db_user = User(**user_data, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: User, user_data: dict) -> User:
        for key, value in user_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> bool:
        self.db.delete(user)
        self.db.commit()
        return True

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active
