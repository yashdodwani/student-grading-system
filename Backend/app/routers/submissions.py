from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import uuid
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole
from app.models.course import Course, StudentCourse
from app.models.assignment import Assignment, Question
from app.models.submission import Submission, Answer, Grade, SubmissionStatus
from app.schemas.submission import (
    SubmissionCreate, SubmissionResponse, SubmissionDetailResponse,
    GradeCreate, GradeResponse
)
from app.utils.auth import get_current_user, get_current_teacher, get_current_student

router = APIRouter(tags=["Submissions"])


@router.get("/api/assignments/{assignment_id}/submissions", response_model=List[SubmissionResponse])
async def get_submissions_by_assignment(
        assignment_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Get all submissions for an assignment (teachers only)."""
    # Check if assignment exists
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
            detail="Not authorized to view submissions for this assignment"
        )

    # Get submissions
    submissions = db.query(Submission) \
        .filter(Submission.assignmentId == assignment_id) \
        .all()

    return submissions


@router.get("/api/students/{student_id}/submissions", response_model=List[SubmissionResponse])
async def get_submissions_by_student(
        student_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get all submissions by a student (self or teacher)."""
    # Students can only view their own submissions
    if current_user.role == UserRole.STUDENT and current_user.id != student_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other students' submissions"
        )

    # For teachers, check if student is in any of their courses
    if current_user.role == UserRole.TEACHER:
        # Get courses taught by the teacher
        teacher_courses = db.query(Course) \
            .filter(Course.teacherId == current_user.id) \
            .all()

        teacher_course_ids = [c.id for c in teacher_courses]

        # Check if student is enrolled in any of these courses
        student_enrollments = db.query(StudentCourse) \
            .filter(
            StudentCourse.studentId == student_id,
            StudentCourse.courseId.in_(teacher_course_ids)
        ) \
            .first()

        if not student_enrollments:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this student's submissions"
            )

    # Get submissions
    submissions = db.query(Submission) \
        .filter(Submission.studentId == student_id) \
        .all()

    return submissions


@router.get("/api/submissions/{submission_id}", response_model=SubmissionDetailResponse)
async def get_submission_by_id(
        submission_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """Get a specific submission by ID with its answers and grade."""
    # Get submission with answers and grade
    submission = db.query(Submission) \
        .options(
        joinedload(Submission.answers),
        joinedload(Submission.grade)
    ) \
        .filter(Submission.id == submission_id) \
        .first()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    # Check permissions
    if current_user.role == UserRole.STUDENT:
        # Students can only view their own submissions
        if submission.studentId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this submission"
            )
    else:  # Teacher
        # Get the assignment and course
        assignment = db.query(Assignment) \
            .filter(Assignment.id == submission.assignmentId) \
            .first()

        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )

        course = db.query(Course) \
            .filter(Course.id == assignment.courseId) \
            .first()

        # Check if teacher owns the course
        if not course or course.teacherId != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this submission"
            )

    return submission


@router.post("/api/assignments/{assignment_id}/submissions", response_model=SubmissionDetailResponse)
async def create_submission(
        assignment_id: str,
        submission_data: SubmissionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_student)
):
    """Create a new submission with answers (students only)."""
    # Check if assignment exists
    assignment = db.query(Assignment) \
        .options(joinedload(Assignment.questions)) \
        .filter(Assignment.id == assignment_id) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    # Check if student is enrolled in the course
    student_enrollment = db.query(StudentCourse) \
        .filter(
        StudentCourse.studentId == current_user.id,
        StudentCourse.courseId == assignment.courseId
    ) \
        .first()

    if not student_enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enrolled in this course"
        )

    # Check if assignment ID in path matches assignmentId in submission data
    if assignment_id != submission_data.assignmentId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment ID mismatch"
        )

    # Check if student already has a submission for this assignment
    existing_submission = db.query(Submission) \
        .filter(
        Submission.studentId == current_user.id,
        Submission.assignmentId == assignment_id
    ) \
        .first()

    if existing_submission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already submitted this assignment"
        )

    # Create new submission
    new_submission = Submission(
        id=str(uuid.uuid4()),
        studentId=current_user.id,
        assignmentId=assignment_id,
        submittedAt=datetime.utcnow(),
        status=SubmissionStatus.SUBMITTED
    )

    db.add(new_submission)

    # Validate questions and create answers
    question_ids = {q.id for q in assignment.questions}
    submission_question_ids = {a.questionId for a in submission_data.answers}

    # Check if all required questions are answered
    if question_ids != submission_question_ids:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All questions must be answered"
        )

    # Add answers
    for answer_data in submission_data.answers:
        # Check if question exists in this assignment
        if answer_data.questionId not in question_ids:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {answer_data.questionId} is not part of this assignment"
            )

        new_answer = Answer(
            id=str(uuid.uuid4()),
            submissionId=new_submission.id,
            questionId=answer_data.questionId,
            text=answer_data.text
        )

        db.add(new_answer)

    db.commit()
    db.refresh(new_submission)

    # Load answers
    answers = db.query(Answer) \
        .filter(Answer.submissionId == new_submission.id) \
        .all()

    new_submission.answers = answers

    return new_submission


@router.post("/api/submissions/{submission_id}/grade", response_model=GradeResponse)
async def grade_submission(
        submission_id: str,
        grade_data: GradeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Grade a submission (teachers only)."""
    # Check if submission exists
    submission = db.query(Submission) \
        .filter(Submission.id == submission_id) \
        .first()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    # Check if teacher has permission to grade this submission
    assignment = db.query(Assignment) \
        .filter(Assignment.id == submission.assignmentId) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    course = db.query(Course) \
        .filter(Course.id == assignment.courseId) \
        .first()

    if not course or course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to grade submissions for this assignment"
        )

    # Check if submission already has a grade
    existing_grade = db.query(Grade) \
        .filter(Grade.submissionId == submission_id) \
        .first()

    if existing_grade:
        # Update existing grade
        existing_grade.grade = grade_data.grade
        existing_grade.comment = grade_data.comment
        existing_grade.gradedAt = datetime.utcnow()

        # Update submission status
        submission.status = SubmissionStatus.GRADED

        db.commit()
        db.refresh(existing_grade)

        return existing_grade
    else:
        # Create new grade
        new_grade = Grade(
            submissionId=submission_id,
            grade=grade_data.grade,
            comment=grade_data.comment,
            gradedAt=datetime.utcnow()
        )

        # Update submission status
        submission.status = SubmissionStatus.GRADED

        db.add(new_grade)
        db.commit()
        db.refresh(new_grade)

        return new_grade


@router.put("/api/submissions/{submission_id}/grade", response_model=GradeResponse)
async def update_grade(
        submission_id: str,
        grade_data: GradeCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_teacher)
):
    """Update the grade for a submission (teachers only)."""
    # Check if submission exists
    submission = db.query(Submission) \
        .filter(Submission.id == submission_id) \
        .first()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    # Check if teacher has permission to grade this submission
    assignment = db.query(Assignment) \
        .filter(Assignment.id == submission.assignmentId) \
        .first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )

    course = db.query(Course) \
        .filter(Course.id == assignment.courseId) \
        .first()

    if not course or course.teacherId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update grades for this assignment"
        )

    # Check if grade exists
    grade = db.query(Grade) \
        .filter(Grade.submissionId == submission_id) \
        .first()

    if not grade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found for this submission"
        )

    # Update grade
    grade.grade = grade_data.grade
    grade.comment = grade_data.comment
    grade.gradedAt = datetime.utcnow()

    db.commit()
    db.refresh(grade)

    return grade


@router.delete("/api/submissions/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_submission(
        submission_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_student)
):
    """Delete a submission (only allowed for own submissions and if not yet graded)."""
    # Get submission
    submission = db.query(Submission) \
        .filter(Submission.id == submission_id) \
        .first()

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )

    # Check if student owns this submission
    if submission.studentId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this submission"
        )

    # Check if submission is already graded
    if submission.status == SubmissionStatus.GRADED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a submission that has already been graded"
        )

    # Delete associated answers
    db.query(Answer) \
        .filter(Answer.submissionId == submission_id) \
        .delete()

    # Delete submission
    db.delete(submission)
    db.commit()

    return None