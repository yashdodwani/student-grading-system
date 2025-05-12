import argparse
import uuid
from datetime import datetime, timedelta
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

sys.path.append(".")  # Add the current directory to the path

from app.database import engine, Base
from app.models.user import User, UserRole
from app.models.course import Course, StudentCourse
from app.models.assignment import Assignment, Question
from app.utils.auth import get_password_hash

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database with tables and seed data."""
    # Check if the database is already initialized
    if inspect(engine).has_table("users"):
        print("Database already initialized.")
        return

    print("Initializing database...")

    # Create tables if they don't exist
    Base.metadata.bind = engine
    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    db = SessionLocal()

    try:
        # Check if admin user exists
        admin = db.query(User).filter(User.email == "admin@example.com").first()

        if not admin:
            print("Creating admin user...")
            admin = User(
                id=str(uuid.uuid4()),
                name="Admin User",
                email="admin@example.com",
                password=get_password_hash("Admin123!"),
                role=UserRole.TEACHER,
                createdAt=datetime.utcnow()
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"Admin user created with ID: {admin.id}")
        else:
            print("Admin user already exists.")

        # Create sample teacher if not exists
        teacher = db.query(User).filter(User.email == "teacher@example.com").first()

        if not teacher:
            print("Creating sample teacher...")
            teacher = User(
                id=str(uuid.uuid4()),
                name="John Doe",
                email="teacher@example.com",
                password=get_password_hash("Teacher123!"),
                role=UserRole.TEACHER,
                createdAt=datetime.utcnow()
            )
            db.add(teacher)
            db.commit()
            db.refresh(teacher)
            print(f"Sample teacher created with ID: {teacher.id}")
        else:
            print("Sample teacher already exists.")

        # Create sample student if not exists
        student = db.query(User).filter(User.email == "student@example.com").first()

        if not student:
            print("Creating sample student...")
            student = User(
                id=str(uuid.uuid4()),
                name="Jane Smith",
                email="student@example.com",
                password=get_password_hash("Student123!"),
                role=UserRole.STUDENT,
                createdAt=datetime.utcnow()
            )
            db.add(student)
            db.commit()
            db.refresh(student)
            print(f"Sample student created with ID: {student.id}")
        else:
            print("Sample student already exists.")

        # Create sample course if not exists
        course = db.query(Course).filter(Course.name == "Introduction to Computer Science").first()

        if not course:
            print("Creating sample course...")
            course = Course(
                id=str(uuid.uuid4()),
                name="Introduction to Computer Science",
                description="A beginner-friendly introduction to computer science concepts",
                teacherId=teacher.id,
                createdAt=datetime.utcnow()
            )
            db.add(course)
            db.commit()
            db.refresh(course)
            print(f"Sample course created with ID: {course.id}")
        else:
            print("Sample course already exists.")

        # Enroll student in course if not already enrolled
        enrollment = db.query(StudentCourse).filter(
            StudentCourse.studentId == student.id,
            StudentCourse.courseId == course.id
        ).first()

        if not enrollment:
            print("Enrolling student in course...")
            enrollment = StudentCourse(
                studentId=student.id,
                courseId=course.id,
                enrolledAt=datetime.utcnow()
            )
            db.add(enrollment)
            db.commit()
            print("Student enrolled in course.")
        else:
            print("Student already enrolled in course.")

        # Create sample assignment if not exists
        assignment = db.query(Assignment).filter(
            Assignment.title == "Fundamentals Quiz",
            Assignment.courseId == course.id
        ).first()

        if not assignment:
            print("Creating sample assignment...")
            now = datetime.utcnow()
            due_date = now + timedelta(days=7)

            assignment = Assignment(
                id=str(uuid.uuid4()),
                title="Fundamentals Quiz",
                description="Test your knowledge of basic computer science concepts",
                courseId=course.id,
                dueDate=due_date,
                createdAt=now
            )
            db.add(assignment)
            db.commit()
            db.refresh(assignment)
            print(f"Sample assignment created with ID: {assignment.id}")

            # Create sample questions
            print("Creating sample questions...")

            questions = [
                {
                    "text": "What does CPU stand for?",
                    "points": 5
                },
                {
                    "text": "What is an algorithm?",
                    "points": 5
                },
                {
                    "text": "Explain the difference between RAM and ROM.",
                    "points": 10
                },
                {
                    "text": "What is the purpose of an operating system?",
                    "points": 10
                },
                {
                    "text": "Explain the concept of object-oriented programming.",
                    "points": 15
                }
            ]

            for q_data in questions:
                question = Question(
                    id=str(uuid.uuid4()),
                    assignmentId=assignment.id,
                    text=q_data["text"],
                    points=q_data["points"]
                )
                db.add(question)

            db.commit()
            print(f"Created {len(questions)} sample questions")
        else:
            print("Sample assignment already exists.")

        print("Database initialization complete!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


def create_user(role, email, password, name):
    """Create a user with specified role."""
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User with email {email} already exists.")
            return

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=get_password_hash(password),
            role=role,
            createdAt=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        print(f"User created successfully: {email} ({role.value})")
    except Exception as e:
        print(f"Error creating user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize database and seed data")
    parser.add_argument("--init", action="store_true", help="Initialize database with sample data")
    parser.add_argument("--create-teacher", action="store_true", help="Create a teacher user")
    parser.add_argument("--create-student", action="store_true", help="Create a student user")
    parser.add_argument("--email", help="Email for user creation")
    parser.add_argument("--password", help="Password for user creation")
    parser.add_argument("--name", help="Name for user creation")

    args = parser.parse_args()

    if args.init:
        init_db()
    elif args.create_teacher and args.email and args.password and args.name:
        create_user(UserRole.TEACHER, args.email, args.password, args.name)
    elif args.create_student and args.email and args.password and args.name:
        create_user(UserRole.STUDENT, args.email, args.password, args.name)
    else:
        parser.print_help()