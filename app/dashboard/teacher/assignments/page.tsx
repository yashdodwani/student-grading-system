import type { Metadata } from "next"
import { AssignmentManagement } from "@/components/assignment-management"
import { PageHeader } from "@/components/page-header"

export const metadata: Metadata = {
  title: "Assignment Management | Student Grading System",
  description: "Manage assignments in the grading system",
}

export default function AssignmentsPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Assignment Management" description="Create and manage assignments for your courses" />
      <AssignmentManagement />
    </div>
  )
}
