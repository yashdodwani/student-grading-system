from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Define Base
Base = declarative_base()


# --- Example User model for completeness ---
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    courses_teaching = relationship("Course", back_populates="teacher")
    enrolled_courses = relationship("StudentCourse", back_populates="student")


# --- Course Model ---
class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    teacher_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Relationships
    teacher = relationship("User", back_populates="courses_teaching")
    students = relationship("StudentCourse", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")


# --- StudentCourse Join Table ---
class StudentCourse(Base):
    __tablename__ = "student_courses"

    id = Column(String, primary_key=True, index=True)
    student_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False, index=True)

    # Relationships
    student = relationship("User", back_populates="enrolled_courses")
    course = relationship("Course", back_populates="students")


# --- Optional: Assignment model placeholder ---
class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="assignments")
