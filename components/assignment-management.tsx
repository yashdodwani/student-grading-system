"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Checkbox } from "@/components/ui/checkbox"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { useToast } from "@/components/ui/use-toast"
import { Plus, Eye, MessageSquare } from "lucide-react"

// Mock data for assignments
const initialAssignments = [
  {
    id: 1,
    name: "ADA algorithm project demo",
    course: "CS108",
    weight: 20,
    questionCount: 2,
    deadline: "2023-12-01T23:59:00",
    students: [
      { id: "1bi23is099", name: "Rishika Snehi", status: "Graded", grade: 16, comment: "Excellent!" },
      { id: "1bi23is093", name: "Rakshita", status: "Graded", grade: 19, comment: "good attempt" },
    ],
  },
  {
    id: 2,
    name: "UHV placard submission",
    course: "CS108",
    weight: 30,
    questionCount: 2,
    deadline: "2023-12-15T23:59:00",
    students: [
      { id: "1bi23is123", name: "Spoorthi", status: "Graded", grade:20, comment: "Do a good job!!" },
      { id: "1bi23is002", name: "Alka", status: "Graded", grade: 25, comment: "Well done" },
    ],
  },
  {
    id: 3,
    name: "DMS assignment 1 and 2",
    course: "CS108",
    weight: 50,
    questionCount: 5,
    deadline: "2023-12-31T23:59:00",
    students: [
      {
        id: "1bi23is087",
        name: "Samarth",
        status: "Graded",
        grade: 4,
        comment: "The best answer I would ever seen.",
      },
      { id: "1809853J-I011-0013", name: "Cyx", status: "Graded", grade: 3.7, comment: "Well Done." },
    ],
  },
]

// Mock data for courses
const courses = ["CS101", "CS108", "CS201"]

export function AssignmentManagement() {
  const [assignments, setAssignments] = useState(initialAssignments)
  const [selectedCourse, setSelectedCourse] = useState("CS108")
  const [selectedAssignment, setSelectedAssignment] = useState<any>(null)
  const [selectedStudent, setSelectedStudent] = useState<any>(null)
  const [showStudents, setShowStudents] = useState(false)
  const [showGrading, setShowGrading] = useState(false)
  const router = useRouter()
  const { toast } = useToast()

  // Filter assignments based on selected course
  const filteredAssignments = assignments.filter((assignment) => assignment.course === selectedCourse)

  const handleCreateAssignment = () => {
    router.push("/dashboard/teacher/assignments/new")
  }

  const handleViewStudents = (assignment: any) => {
    setSelectedAssignment(assignment)
    setShowStudents(true)
  }

  const handleGradeStudent = (student: any) => {
    setSelectedStudent({ ...student })
    setShowGrading(true)
  }

  const handleSaveGrade = () => {
    if (selectedStudent && selectedAssignment) {
      const updatedAssignments = assignments.map((assignment) => {
        if (assignment.id === selectedAssignment.id) {
          const updatedStudents = assignment.students.map((student) =>
            student.id === selectedStudent.id ? selectedStudent : student,
          )
          return { ...assignment, students: updatedStudents }
        }
        return assignment
      })

      setAssignments(updatedAssignments)
      setShowGrading(false)
      toast({
        title: "Grade Saved",
        description: `Grade for ${selectedStudent.name} has been updated.`,
      })
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString() + " " + date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Assignment Management</CardTitle>
          <div className="flex items-center gap-4">
            <Select value={selectedCourse} onValueChange={setSelectedCourse}>
              <SelectTrigger className="w-[180px]">
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
            <Button onClick={handleCreateAssignment}>
              <Plus className="mr-2 h-4 w-4" />
              Create Assignment
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Weight (%)</TableHead>
                <TableHead>Questions</TableHead>
                <TableHead>Deadline</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAssignments.map((assignment) => (
                <TableRow key={assignment.id}>
                  <TableCell className="font-medium">{assignment.name}</TableCell>
                  <TableCell>{assignment.weight}</TableCell>
                  <TableCell>{assignment.questionCount}</TableCell>
                  <TableCell>{formatDate(assignment.deadline)}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="bg-green-50 text-green-700 hover:bg-green-50">
                      Active
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button variant="outline" size="sm" className="ml-2" onClick={() => handleViewStudents(assignment)}>
                      <Eye className="mr-2 h-4 w-4" />
                      View Submissions
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {/* Student Submissions Dialog */}
      <Dialog open={showStudents} onOpenChange={setShowStudents}>
        <DialogContent className="max-w-3xl">
          <DialogHeader>
            <DialogTitle>{selectedAssignment?.name} - Student Submissions</DialogTitle>
          </DialogHeader>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Select</TableHead>
                <TableHead>Student ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Grade</TableHead>
                <TableHead>Comment</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {selectedAssignment?.students.map((student: any) => (
                <TableRow key={student.id}>
                  <TableCell>
                    <Checkbox />
                  </TableCell>
                  <TableCell className="font-medium">{student.id}</TableCell>
                  <TableCell>{student.name}</TableCell>
                  <TableCell>
                    <Badge
                      variant={student.status === "Graded" ? "outline" : "secondary"}
                      className={student.status === "Graded" ? "bg-green-50 text-green-700" : ""}
                    >
                      {student.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{student.grade}</TableCell>
                  <TableCell className="max-w-[150px] truncate">{student.comment}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="outline" size="icon" onClick={() => handleGradeStudent(student)}>
                      <MessageSquare className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
      </Dialog>

      {/* Grading Dialog */}
      <Dialog open={showGrading} onOpenChange={setShowGrading}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Grade Assignment</DialogTitle>
          </DialogHeader>
          {selectedStudent && (
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Assignment</label>
                  <p>{selectedAssignment?.name}</p>
                </div>
                <div>
                  <label className="text-sm font-medium">Student</label>
                  <p>{selectedStudent.name}</p>
                </div>
              </div>
              <div className="grid gap-2">
                <label htmlFor="grade" className="text-sm font-medium">
                  Grade
                </label>
                <Input
                  id="grade"
                  type="number"
                  min="0"
                  max="4"
                  step="0.1"
                  value={selectedStudent.grade}
                  onChange={(e) =>
                    setSelectedStudent({
                      ...selectedStudent,
                      grade: Number.parseFloat(e.target.value),
                      status: "Graded",
                    })
                  }
                />
              </div>
              <div className="grid gap-2">
                <label htmlFor="comment" className="text-sm font-medium">
                  Comment
                </label>
                <Textarea
                  id="comment"
                  value={selectedStudent.comment}
                  onChange={(e) => setSelectedStudent({ ...selectedStudent, comment: e.target.value })}
                  placeholder="Add feedback for the student..."
                  rows={4}
                />
              </div>
              <div className="flex justify-end">
                <Button onClick={handleSaveGrade}>Save Grade</Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </>
  )
}
