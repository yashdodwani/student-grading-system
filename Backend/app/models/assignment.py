from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
import datetime


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    courseId = Column(String, ForeignKey("courses.id"), nullable=False)
    weight = Column(Float, nullable=False)
    questionCount = Column(Integer, nullable=False)
    deadline = Column(DateTime, nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    course = relationship("Course", back_populates="assignments")
    questions = relationship("Question", back_populates="assignment")
    submissions = relationship("Submission", back_populates="assignment")


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, index=True)
    assignmentId = Column(String, ForeignKey("assignments.id"), nullable=False)
    text = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    # Relationships
    assignment = relationship("Assignment", back_populates="questions")
    answers = relationship("Answer", back_populates="question")