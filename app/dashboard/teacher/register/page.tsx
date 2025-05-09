import type { Metadata } from "next"
import { RegisterForm } from "@/components/register-form"
import { PageHeader } from "@/components/page-header"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export const metadata: Metadata = {
  title: "Registration | Student Grading System",
  description: "Register new students or courses",
}

export default function RegisterPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Registration" description="Register new students or courses" />

      <Tabs defaultValue="student" className="w-full">
        <TabsList className="grid w-full max-w-md grid-cols-2 mb-6">
          <TabsTrigger value="student">Register Student</TabsTrigger>
          <TabsTrigger value="course">Register Course</TabsTrigger>
        </TabsList>
        <TabsContent value="student">
          <RegisterForm type="student" />
        </TabsContent>
        <TabsContent value="course">
          <RegisterForm type="course" />
        </TabsContent>
      </Tabs>
    </div>
  )
}
