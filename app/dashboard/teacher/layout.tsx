import type React from "react"
import { TeacherSidebar } from "@/components/teacher-sidebar"

export default function TeacherDashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <TeacherSidebar />
      <div className="flex-1 p-6 lg:p-8">{children}</div>
    </div>
  )
}
