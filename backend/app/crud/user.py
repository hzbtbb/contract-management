from sqlalchemy.orm import Session
from app.models.models import User, Contract
from app.core.security import get_password_hash, verify_password
from typing import Optional

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password: str, department: str = None, role: str = "user") -> User:
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        hashed_password=hashed_password,
        department=department,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, role: str = None, department: str = None) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    old_department = user.department

    if role is not None:
        user.role = role
    if department is not None:
        user.department = department
        # 更新该用户上传的所有合同的科室
        if old_department and old_department != department:
            db.query(Contract).filter(Contract.uploader_id == user_id).update({"department": department})

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
