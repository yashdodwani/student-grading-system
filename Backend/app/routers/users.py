from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.utils.auth import get_current_user, get_current_teacher, get_password_hash

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_all_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Get all users (teachers only)."""
    users = db.query(User).all()
    return users


@router.get("/teachers", response_model=List[UserResponse])
async def get_all_teachers(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all teachers."""
    teachers = db.query(User).filter(User.role == UserRole.TEACHER).all()
    return teachers


@router.get("/students", response_model=List[UserResponse])
async def get_all_students(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all students."""
    students = db.query(User).filter(User.role == UserRole.STUDENT).all()
    return students


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
        user_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get a specific user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
        user_id: str,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Update a user (self or teacher only)."""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if current user has permission to update this user
    if current_user.id != user_id and current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # Update user data
    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        # Check if email already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user.email = user_data.email

    if user_data.password is not None:
        user.password = get_password_hash(user_data.password)

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Delete a user (teachers only)."""
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Delete user
    db.delete(user)
    db.commit()

    return None