from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid

from app.database import get_db
from app.models.user import User, UserRole
from app.models.course import Course, StudentCourse
from app.schemas.course import CourseCreate, CourseResponse, CourseDetailResponse, CourseUpdate, StudentEnrollment
from app.schemas.user import UserResponse
from app.utils.auth import get_current_user, get_current_teacher

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.get("/", response_model=List[CourseResponse])
async def get_all_courses(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all courses (for teachers) or enrolled courses (for students)."""
    if current_user.role == UserRole.TEACHER:
        courses = db.query(Course).all()
    else:
        # For students, get only enrolled courses
        enrollments = db.query(StudentCourse).filter(StudentCourse.studentId == current_user.id).all()
        course_ids = [enrollment.courseId for enrollment in enrollments]
        courses = db.query(Course).filter(Course.id.in_(course_ids)).all()

    return courses


@router.post("/", response_model=CourseResponse)
async def create_course(
        course_data: CourseCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Create a new course (teachers only)."""
    new_course = Course(
        id=str(uuid.uuid4()),
        name=course_data.name,
        teacherId=current_user.id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course_by_id(
        course_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get a specific course by ID."""
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if student is enrolled or user is a teacher
    if current_user.role == UserRole.STUDENT:
        enrollment = db.query(StudentCourse).filter(
            StudentCourse.studentId == current_user.id,
            StudentCourse.courseId == course_id
        ).first()

        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enrolled in this course"
            )

    # Count number of students enrolled
    student_count = db.query(StudentCourse).filter(StudentCourse.courseId == course_id).count()

    # Create response with student count
    response = CourseDetailResponse(
        id=course.id,
        name=course.name,
        teacherId=course.teacherId,
        student_count=student_count
    )

    return response


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
        course_id: str,
        course_data: CourseUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Update a course (teachers only)."""
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the teacher of this course
    if course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this course"
        )

    # Update course data
    if course_data.name is not None:
        course.name = course_data.name

    db.commit()
    db.refresh(course)

    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
        course_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Delete a course (teachers only)."""
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the teacher of this course
    if course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this course"
        )

    # Delete course
    db.delete(course)
    db.commit()

    return None


@router.get("/{course_id}/students", response_model=List[UserResponse])
async def get_course_students(
        course_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Get all students enrolled in a course (teachers only)."""
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the teacher of this course
    if course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view students of this course"
        )

    # Get all students enrolled in this course
    enrollments = db.query(StudentCourse).filter(StudentCourse.courseId == course_id).all()
    student_ids = [enrollment.studentId for enrollment in enrollments]
    students = db.query(User).filter(User.id.in_(student_ids)).all()

    return students


@router.post("/{course_id}/students", response_model=CourseDetailResponse)
async def add_student_to_course(
        course_id: str,
        student_data: StudentEnrollment,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Add a student to a course (teachers only)."""
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the teacher of this course
    if course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add students to this course"
        )

    # Check if student exists
    student = db.query(User).filter(
        User.id == student_data.studentId,
        User.role == UserRole.STUDENT
    ).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    # Check if student is already enrolled
    existing_enrollment = db.query(StudentCourse).filter(
        StudentCourse.studentId == student_data.studentId,
        StudentCourse.courseId == course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled in this course"
        )

    # Create new enrollment
    new_enrollment = StudentCourse(
        studentId=student_data.studentId,
        courseId=course_id
    )

    db.add(new_enrollment)
    db.commit()

    # Get updated student count
    student_count = db.query(StudentCourse).filter(StudentCourse.courseId == course_id).count()

    # Create response
    response = CourseDetailResponse(
        id=course.id,
        name=course.name,
        teacherId=course.teacherId,
        student_count=student_count
    )

    return response


@router.delete("/{course_id}/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_student_from_course(
        course_id: str,
        student_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Remove a student from a course (teachers only)."""
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the teacher of this course
    if course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to remove students from this course"
        )

    # Check if enrollment exists
    enrollment = db.query(StudentCourse).filter(
        StudentCourse.studentId == student_id,
        StudentCourse.courseId == course_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not enrolled in this course"
        )

    # Delete enrollment
    db.delete(enrollment)
    db.commit()

    return None