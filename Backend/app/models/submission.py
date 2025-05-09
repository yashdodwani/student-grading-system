from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base
import enum
import datetime


class SubmissionStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    GRADED = "graded"


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, index=True)
    studentId = Column(String, ForeignKey("users.id"), nullable=False)
    assignmentId = Column(String, ForeignKey("assignments.id"), nullable=False)
    submittedAt = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.SUBMITTED)

    # Relationships
    student = relationship("User", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    answers = relationship("Answer", back_populates="submission")
    grade = relationship("Grade", back_populates="submission", uselist=False)


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, index=True)
    submissionId = Column(String, ForeignKey("submissions.id"), nullable=False)
    questionId = Column(String, ForeignKey("questions.id"), nullable=False)
    text = Column(Text, nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="answers")
    question = relationship("Question", back_populates="answers")


class Grade(Base):
    __tablename__ = "grades"

    submissionId = Column(String, ForeignKey("submissions.id"), primary_key=True)
    grade = Column(Float, nullable=False)
    comment = Column(Text)
    gradedAt = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    submission = relationship("Submission", back_populates="grade")