import type { Metadata } from "next"
import { NewAssignmentForm } from "@/components/new-assignment-form"
import { PageHeader } from "@/components/page-header"

export const metadata: Metadata = {
  title: "Create Assignment | Student Grading System",
  description: "Create a new assignment",
}

export default function NewAssignmentPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Create New Assignment" description="Add a new assignment to your course" />
      <NewAssignmentForm />
    </div>
  )
}
