from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Base Course Schema
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    code: str = Field(..., description="Unique course code like CS101")


# Schema for course creation
class CourseCreate(CourseBase):
    pass


# Schema for course update
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    code: Optional[str] = None


# Schema for simple course response
class CourseResponse(CourseBase):
    id: str
    instructorId: str
    createdAt: datetime
    updatedAt: Optional[datetime] = None

    class Config:
        from_attributes = True


# Schema for enrolling students
class StudentEnrollment(BaseModel):
    studentIds: List[str]


# Schema for detailed course response (includes enrollment info)
class CourseDetailResponse(CourseResponse):
    studentCount: int = 0
    assignmentCount: int = 0
    # Could include other aggregate data like average grades, etc.

    class Config:
        from_attributes = True