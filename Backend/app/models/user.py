from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

# Define Base
Base = declarative_base()


class UserRole(str, enum.Enum):
    TEACHER = "teacher"
    STUDENT = "student"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # Hashed password
    role = Column(Enum(UserRole), nullable=False)

    # Relationships
    courses_teaching = relationship("Course", back_populates="teacher")
    enrolled_courses = relationship("StudentCourse", back_populates="student")
    submissions = relationship("Submission", back_populates="student")