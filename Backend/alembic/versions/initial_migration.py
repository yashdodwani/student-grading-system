"""Initial migration

Revision ID: 8a9eb1c0c4a1
Revises:
Create Date: 2025-05-09 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8a9eb1c0c4a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create enum type for user roles
    op.create_table(
        'users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('STUDENT', 'TEACHER', name='userrole'), nullable=False),
        sa.Column('createdAt', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create courses table
    op.create_table(
        'courses',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('teacherId', sa.String(), nullable=False),
        sa.Column('createdAt', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['teacherId'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create student_courses table (many-to-many relationship)
    op.create_table(
        'student_courses',
        sa.Column('studentId', sa.String(), nullable=False),
        sa.Column('courseId', sa.String(), nullable=False),
        sa.Column('enrolledAt', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['courseId'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['studentId'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('studentId', 'courseId')
    )

    # Create assignments table
    op.create_table(
        'assignments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('courseId', sa.String(), nullable=False),
        sa.Column('dueDate', sa.DateTime(), nullable=True),
        sa.Column('createdAt', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['courseId'], ['courses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create questions table
    op.create_table(
        'questions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('assignmentId', sa.String(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['assignmentId'], ['assignments.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create submissions table
    op.create_table(
        'submissions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('studentId', sa.String(), nullable=False),
        sa.Column('assignmentId', sa.String(), nullable=False),
        sa.Column('submittedAt', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('SUBMITTED', 'GRADED', name='submissionstatus'), nullable=False),
        sa.ForeignKeyConstraint(['assignmentId'], ['assignments.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['studentId'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('studentId', 'assignmentId')
    )

    # Create answers table
    op.create_table(
        'answers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('submissionId', sa.String(), nullable=False),
        sa.Column('questionId', sa.String(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['questionId'], ['questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['submissionId'], ['submissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('submissionId', 'questionId')
    )

    # Create grades table
    op.create_table(
        'grades',
        sa.Column('submissionId', sa.String(), nullable=False),
        sa.Column('grade', sa.Float(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('gradedAt', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['submissionId'], ['submissions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('submissionId')
    )


def downgrade():
    # Drop tables in reverse order of creation to maintain referential integrity
    op.drop_table('grades')
    op.drop_table('answers')
    op.drop_table('submissions')
    op.drop_table('questions')
    op.drop_table('assignments')
    op.drop_table('student_courses')
    op.drop_table('courses')
    op.drop_table('users')

    # Drop enum types
    op.execute('DROP TYPE submissionstatus')
    op.execute('DROP TYPE userrole')