from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Base Question Schema
class QuestionBase(BaseModel):
    text: str
    order: int

# Schema for question creation
class QuestionCreate(QuestionBase):
    pass

# Schema for question response
class QuestionResponse(QuestionBase):
    id: str
    assignmentId: str

    class Config:
        from_attributes = True

# Base Assignment Schema
class AssignmentBase(BaseModel):
    name: str
    weight: float = Field(..., ge=0, le=100)
    questionCount: int = Field(..., gt=0)
    deadline: datetime

# Schema for assignment creation
class AssignmentCreate(AssignmentBase):
    questions: List[QuestionBase]

# Schema for assignment update
class AssignmentUpdate(BaseModel):
    name: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0, le=100)
    deadline: Optional[datetime] = None

# Schema for assignment response
class AssignmentResponse(AssignmentBase):
    id: str
    courseId: str
    createdAt: datetime

    class Config:
        from_attributes = True

# Schema for detailed assignment response (includes questions)
class AssignmentDetailResponse(AssignmentResponse):
    questions: List[QuestionResponse] = []

    class Config:
        from_attributes = True