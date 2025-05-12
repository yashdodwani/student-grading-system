import re
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime


def validate_email(email: str) -> str:
    """
    Validate email format.

    Args:
        email: The email to validate

    Returns:
        The validated email

    Raises:
        HTTPException: If email is invalid
    """
    # Simple email pattern validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    return email.lower()


def validate_password_strength(password: str) -> str:
    """
    Validate password strength.

    Args:
        password: The password to validate

    Returns:
        The validated password

    Raises:
        HTTPException: If password doesn't meet criteria
    """
    # Password must be at least 8 characters and contain at least one
    # lowercase letter, one uppercase letter, one digit, and one special character
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    if not re.search(r'[a-z]', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one lowercase letter"
        )

    if not re.search(r'[A-Z]', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one uppercase letter"
        )

    if not re.search(r'\d', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one digit"
        )

    if not re.search(r'[!@#$%^&*()-=_+[\]{}|;:\'",.<>/?]', password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least one special character"
        )

    return password


def validate_date_range(start_date: datetime, end_date: Optional[datetime] = None) -> None:
    """
    Validate date range.

    Args:
        start_date: The start date
        end_date: The end date (optional)

    Raises:
        HTTPException: If dates are invalid
    """
    if end_date and start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )


def validate_uuid(uuid_str: str) -> str:
    """
    Validate UUID format.

    Args:
        uuid_str: The UUID string to validate

    Returns:
        The validated UUID string

    Raises:
        HTTPException: If UUID format is invalid
    """
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(pattern, uuid_str.lower()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format"
        )
    return uuid_str


def validate_grade(grade: float) -> float:
    """
    Validate grade is within acceptable range (0-100).

    Args:
        grade: The grade to validate

    Returns:
        The validated grade

    Raises:
        HTTPException: If grade is outside valid range
    """
    if grade < 0 or grade > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Grade must be between 0 and 100"
        )
    return grade