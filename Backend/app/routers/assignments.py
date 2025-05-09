from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid

from app.database import get_db
from app.models.user import User, UserRole
from app.models.course import Course, StudentCourse
from app.models.assignment import Assignment, Question
from app.schemas.assignment import (
    AssignmentCreate, AssignmentResponse, AssignmentDetailResponse,
    AssignmentUpdate, QuestionResponse
)
from app.utils.auth import get_current_user, get_current_teacher

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])


@router.get("/", response_model=List[AssignmentResponse])
async def get_all_assignments(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all assignments (for teachers) or assignments for enrolled courses (for students)."""
    if current_user.role == UserRole.TEACHER:
        # Teachers can see all assignments they created
        assignments = db.query(Assignment) \
            .join(Course) \
            .filter(Course.teacherId == current_user.id) \
            .all()
    else:
        # Students can see assignments for courses they're enrolled in
        student_courses = db.query(StudentCourse) \
            .filter(StudentCourse.studentId == current_user.id) \
            .all()
        course_ids = [sc.courseId for sc in student_courses]
        assignments = db.query(Assignment) \
            .filter(Assignment.courseId.in_(course_ids)) \
            .all()

    return assignments


@router.get("/{assignment_id}", response_model=AssignmentDetailResponse)
async def get_assignment_by_id(
        assignment_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get a specific assignment by ID with its questions."""
    # Get assignment with questions
    assignment = db.query(Assignment) \
        .options(joinedload(Assignment.questions)) \
        .filter(Assignment.id == assignment_id) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # Check if user has access to this assignment
    if current_user.role == UserRole.TEACHER:
        course = db.query(Course) \
            .filter(Course.id == assignment.courseId) \
            .first()

        if not course or course.teacherId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this assignment"
            )
    else:
        # Check if student is enrolled in the course
        enrollment = db.query(StudentCourse) \
            .filter(
            StudentCourse.studentId == current_user.id,
            StudentCourse.courseId == assignment.courseId
        ) \
            .first()

        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enrolled in the course for this assignment"
            )

    # Sort questions by order
    assignment.questions.sort(key=lambda x: x.order)

    return assignment


@router.post("/", response_model=AssignmentDetailResponse)
async def create_assignment(
        assignment_data: AssignmentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Create a new assignment with questions (teachers only)."""
    # Check if course exists and teacher owns it
    course = db.query(Course) \
        .filter(Course.id == assignment_data.courseId) \
        .first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create assignments for this course"
        )

    # Validate that the number of questions matches questionCount
    if len(assignment_data.questions) != assignment_data.questionCount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Number of questions ({len(assignment_data.questions)}) doesn't match questionCount ({assignment_data.questionCount})"
        )

    # Create assignment
    assignment_id = str(uuid.uuid4())
    new_assignment = Assignment(
        id=assignment_id,
        name=assignment_data.name,
        courseId=assignment_data.courseId,
        weight=assignment_data.weight,
        questionCount=assignment_data.questionCount,
        deadline=assignment_data.deadline
    )

    db.add(new_assignment)

    # Create questions
    questions = []
    for i, question_data in enumerate(assignment_data.questions):
        new_question = Question(
            id=str(uuid.uuid4()),
            assignmentId=assignment_id,
            text=question_data.text,
            order=question_data.order
        )
        db.add(new_question)
        questions.append(new_question)

    db.commit()

    # Create response
    response = AssignmentDetailResponse(
        id=new_assignment.id,
        name=new_assignment.name,
        courseId=new_assignment.courseId,
        weight=new_assignment.weight,
        questionCount=new_assignment.questionCount,
        deadline=new_assignment.deadline,
        createdAt=new_assignment.createdAt,
        questions=questions
    )

    return response


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
        assignment_id: str,
        assignment_data: AssignmentUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Update an assignment (teachers only)."""
    # Get assignment
    assignment = db.query(Assignment) \
        .filter(Assignment.id == assignment_id) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # Check if teacher owns the course
    course = db.query(Course) \
        .filter(Course.id == assignment.courseId) \
        .first()

    if not course or course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this assignment"
        )

    # Update assignment data
    if assignment_data.name is not None:
        assignment.name = assignment_data.name

    if assignment_data.weight is not None:
        assignment.weight = assignment_data.weight

    if assignment_data.deadline is not None:
        assignment.deadline = assignment_data.deadline

    db.commit()
    db.refresh(assignment)

    return assignment


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
        assignment_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Delete an assignment (teachers only)."""
    # Get assignment
    assignment = db.query(Assignment) \
        .filter(Assignment.id == assignment_id) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # Check if teacher owns the course
    course = db.query(Course) \
        .filter(Course.id == assignment.courseId) \
        .first()

    if not course or course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this assignment"
        )

    # Delete assignment (cascade will delete questions)
    db.delete(assignment)
    db.commit()

    return None


@router.get("/{assignment_id}/questions", response_model=List[QuestionResponse])
async def get_assignment_questions(
        assignment_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get questions for an assignment."""
    # Get assignment
    assignment = db.query(Assignment) \
        .filter(Assignment.id == assignment_id) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # Check if user has access to this assignment
    if current_user.role == UserRole.TEACHER:
        course = db.query(Course) \
            .filter(Course.id == assignment.courseId) \
            .first()

        if not course or course.teacherId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this assignment"
            )
    else:
        # Check if student is enrolled in the course
        enrollment = db.query(StudentCourse) \
            .filter(
            StudentCourse.studentId == current_user.id,
            StudentCourse.courseId == assignment.courseId
        ) \
            .first()

        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enrolled in the course for this assignment"
            )

    # Get questions sorted by order
    questions = db.query(Question) \
        .filter(Question.assignmentId == assignment_id) \
        .order_by(Question.order) \
        .all()

    return questions