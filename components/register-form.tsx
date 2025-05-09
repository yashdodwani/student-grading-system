"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/components/ui/use-toast"

interface RegisterFormProps {
  type: "student" | "course"
}

export function RegisterForm({ type }: RegisterFormProps) {
  const router = useRouter()
  const { toast } = useToast()

  const [studentFormData, setStudentFormData] = useState({
    studentId: "",
    name: "",
    password: "",
    email: "",
    courseId: "",
    courseName: "",
  })

  const [courseFormData, setCourseFormData] = useState({
    courseId: "",
    courseName: "",
  })

  const handleStudentInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setStudentFormData({
      ...studentFormData,
      [name]: value,
    })
  }

  const handleCourseInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setCourseFormData({
      ...courseFormData,
      [name]: value,
    })
  }

  const handleStudentSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate form
    if (!studentFormData.studentId || !studentFormData.name || !studentFormData.courseId) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive",
      })
      return
    }

    // In a real app, you would send this data to your backend
    console.log("Student registration data:", studentFormData)

    toast({
      title: "Student Registered",
      description: `${studentFormData.name} has been registered successfully.`,
    })

    // Reset form
    setStudentFormData({
      studentId: "",
      name: "",
      password: "",
      email: "",
      courseId: "",
      courseName: "",
    })
  }

  const handleCourseSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate form
    if (!courseFormData.courseId || !courseFormData.courseName) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive",
      })
      return
    }

    // In a real app, you would send this data to your backend
    console.log("Course registration data:", courseFormData)

    toast({
      title: "Course Registered",
      description: `${courseFormData.courseName} has been registered successfully.`,
    })

    // Reset form
    setCourseFormData({
      courseId: "",
      courseName: "",
    })
  }

  const handleCancel = () => {
    router.push("/dashboard/teacher")
  }

  if (type === "student") {
    return (
      <form onSubmit={handleStudentSubmit}>
        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="studentId">Student ID</Label>
                <Input
                  id="studentId"
                  name="studentId"
                  value={studentFormData.studentId}
                  onChange={handleStudentInputChange}
                  placeholder="e.g., 1809853Z-I011-0045"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name">Student Name</Label>
                <Input
                  id="name"
                  name="name"
                  value={studentFormData.name}
                  onChange={handleStudentInputChange}
                  placeholder="e.g., John Smith"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  value={studentFormData.password}
                  onChange={handleStudentInputChange}
                  placeholder="Create a password"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email Address</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={studentFormData.email}
                  onChange={handleStudentInputChange}
                  placeholder="e.g., john.smith@example.com"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="courseId">Course ID</Label>
                <Input
                  id="courseId"
                  name="courseId"
                  value={studentFormData.courseId}
                  onChange={handleStudentInputChange}
                  placeholder="e.g., CS108"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="courseName">Course Name</Label>
                <Input
                  id="courseName"
                  name="courseName"
                  value={studentFormData.courseName}
                  onChange={handleStudentInputChange}
                  placeholder="e.g., Advanced Database"
                />
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button type="button" variant="outline" onClick={handleCancel}>
              Cancel
            </Button>
            <Button type="submit">Register Student</Button>
          </CardFooter>
        </Card>
      </form>
    )
  }

  return (
    <form onSubmit={handleCourseSubmit}>
      <Card>
        <CardContent className="pt-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="courseId">Course ID</Label>
              <Input
                id="courseId"
                name="courseId"
                value={courseFormData.courseId}
                onChange={handleCourseInputChange}
                placeholder="e.g., CS108"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="courseName">Course Name</Label>
              <Input
                id="courseName"
                name="courseName"
                value={courseFormData.courseName}
                onChange={handleCourseInputChange}
                placeholder="e.g., Advanced Database"
              />
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button type="button" variant="outline" onClick={handleCancel}>
            Cancel
          </Button>
          <Button type="submit">Register Course</Button>
        </CardFooter>
      </Card>
    </form>
  )
}
