import type { Metadata } from "next"
import { StudentManagement } from "@/components/student-management"
import { PageHeader } from "@/components/page-header"

export const metadata: Metadata = {
  title: "Student Management | Student Grading System",
  description: "Manage students in the grading system",
}

export default function StudentsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Student Management" description="View and manage students in your courses" />
      <StudentManagement />
    </div>
  )
}
