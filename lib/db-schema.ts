// This file defines the database schema for the student grading system

export type User = {
  id: string
  name: string
  email: string
  password: string // In a real app, this would be hashed
  role: "teacher" | "student"
}

export type Course = {
  id: string
  name: string
  teacherId: string
}

export type StudentCourse = {
  studentId: string
  courseId: string
}

export type Assignment = {
  id: string
  name: string
  courseId: string
  weight: number
  questionCount: number
  deadline: string
  createdAt: string
}

export type Question = {
  id: string
  assignmentId: string
  text: string
  order: number
}

export type Submission = {
  id: string
  studentId: string
  assignmentId: string
  submittedAt: string
  status: "submitted" | "graded"
}

export type Answer = {
  id: string
  submissionId: string
  questionId: string
  text: string
}

export type Grade = {
  submissionId: string
  grade: number
  comment: string
  gradedAt: string
}
