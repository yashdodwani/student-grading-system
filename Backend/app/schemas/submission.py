from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.submission import SubmissionStatus

# Base Answer Schema
class AnswerBase(BaseModel):
    questionId: str
    text: str

# Schema for answer response
class AnswerResponse(AnswerBase):
    id: str
    submissionId: str

    class Config:
        from_attributes = True

# Base Submission Schema
class SubmissionBase(BaseModel):
    assignmentId: str

# Schema for submission creation
class SubmissionCreate(SubmissionBase):
    answers: List[AnswerBase]

# Schema for submission response
class SubmissionResponse(SubmissionBase):
    id: str
    studentId: str
    submittedAt: datetime
    status: SubmissionStatus

    class Config:
        from_attributes = True

# Schema for detailed submission response (includes answers)
class SubmissionDetailResponse(SubmissionResponse):
    answers: List[AnswerResponse] = []
    grade: Optional['GradeResponse'] = None

    class Config:
        from_attributes = True

# Base Grade Schema
class GradeBase(BaseModel):
    grade: float = Field(..., ge=0, le=100)
    comment: Optional[str] = None

# Schema for grade creation/update
class GradeCreate(GradeBase):
    pass

# Schema for grade response
class GradeResponse(GradeBase):
    submissionId: str
    gradedAt: datetime

    class Config:
        from_attributes = True

# Update forward reference
SubmissionDetailResponse.update_forward_refs()