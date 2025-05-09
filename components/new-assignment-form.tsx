"use client"

import type React from "react"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { useToast } from "@/components/ui/use-toast"
import { Plus, Trash } from "lucide-react"

// Mock data for courses
const courses = ["CS101", "CS108", "CS201"]

export function NewAssignmentForm() {
  const router = useRouter()
  const { toast } = useToast()
  const [formData, setFormData] = useState({
    courseId: "CS108",
    name: "",
    weight: "",
    deadline: "",
    questions: [{ text: "" }, { text: "" }],
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value,
    })
  }

  const handleCourseChange = (value: string) => {
    setFormData({
      ...formData,
      courseId: value,
    })
  }

  const handleQuestionChange = (index: number, value: string) => {
    const updatedQuestions = [...formData.questions]
    updatedQuestions[index] = { text: value }
    setFormData({
      ...formData,
      questions: updatedQuestions,
    })
  }

  const addQuestion = () => {
    setFormData({
      ...formData,
      questions: [...formData.questions, { text: "" }],
    })
  }

  const removeQuestion = (index: number) => {
    const updatedQuestions = formData.questions.filter((_, i) => i !== index)
    setFormData({
      ...formData,
      questions: updatedQuestions,
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Validate form
    if (!formData.name || !formData.weight || !formData.deadline) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive",
      })
      return
    }

    // In a real app, you would send this data to your backend
    console.log("Assignment data:", formData)

    toast({
      title: "Assignment Created",
      description: `${formData.name} has been created successfully.`,
    })

    // Redirect back to assignments page
    router.push("/dashboard/teacher/assignments")
  }

  const handleCancel = () => {
    router.push("/dashboard/teacher/assignments")
  }

  return (
    <form onSubmit={handleSubmit}>
      <Card>
        <CardHeader>
          <CardTitle>Assignment Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="courseId">Course ID</Label>
              <Select value={formData.courseId} onValueChange={handleCourseChange}>
                <SelectTrigger id="courseId">
                  <SelectValue placeholder="Select course" />
                </SelectTrigger>
                <SelectContent>
                  {courses.map((course) => (
                    <SelectItem key={course} value={course}>
                      {course}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <Label htmlFor="name">Assignment Name</Label>
              <Input
                id="name"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
                placeholder="e.g., Midterm Project"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-2">
              <Label htmlFor="weight">Weight (%)</Label>
              <Input
                id="weight"
                name="weight"
                type="number"
                min="0"
                max="100"
                value={formData.weight}
                onChange={handleInputChange}
                placeholder="e.g., 20"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="deadline">Deadline</Label>
              <Input
                id="deadline"
                name="deadline"
                type="datetime-local"
                value={formData.deadline}
                onChange={handleInputChange}
              />
            </div>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label>Questions</Label>
              <Button type="button" variant="outline" size="sm" onClick={addQuestion}>
                <Plus className="mr-2 h-4 w-4" />
                Add Question
              </Button>
            </div>

            {formData.questions.map((question, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor={`question-${index}`}>Question {index + 1}</Label>
                  {formData.questions.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      onClick={() => removeQuestion(index)}
                    >
                      <Trash className="h-4 w-4" />
                    </Button>
                  )}
                </div>
                <Textarea
                  id={`question-${index}`}
                  value={question.text}
                  onChange={(e) => handleQuestionChange(index, e.target.value)}
                  placeholder="Enter your question here..."
                  rows={3}
                />
              </div>
            ))}
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button type="button" variant="outline" onClick={handleCancel}>
            Cancel
          </Button>
          <Button type="submit">Create Assignment</Button>
        </CardFooter>
      </Card>
    </form>
  )
}
