"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { useToast } from "@/components/ui/use-toast"
import { Edit, Trash2, Search } from "lucide-react"

// Mock data for students
const initialStudents = [
  {
    id: "1809853J-I011-0013",
    name: "Cyx",
    password: "cyx667",
    email: "godkillerchen@gmail.com",
    course: "CS108",
  },
  {
    id: "1809853Z-I011-0045",
    name: "Kennard Wang",
    password: "wyy1809",
    email: "wangkennard@gmail.com",
    course: "CS108",
  },
  {
    id: "1909853U-I011-0151",
    name: "Kiera Yi",
    password: "yz123456",
    email: "yz@gmail.com",
    course: "CS108",
  },
]

// Mock data for courses
const courses = ["CS101", "CS108", "CS201"]

export function StudentManagement() {
  const [students, setStudents] = useState(initialStudents)
  const [selectedCourse, setSelectedCourse] = useState("CS108")
  const [searchQuery, setSearchQuery] = useState("")
  const [editingStudent, setEditingStudent] = useState<any>(null)
  const { toast } = useToast()

  // Filter students based on selected course and search query
  const filteredStudents = students.filter(
    (student) =>
      student.course === selectedCourse &&
      (searchQuery === "" ||
        student.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        student.email.toLowerCase().includes(searchQuery.toLowerCase())),
  )

  const handleEdit = (student: any) => {
    setEditingStudent({ ...student })
  }

  const handleSaveEdit = () => {
    if (editingStudent) {
      setStudents(students.map((s) => (s.id === editingStudent.id ? editingStudent : s)))
      setEditingStudent(null)
      toast({
        title: "Student Updated",
        description: `${editingStudent.name}'s information has been updated.`,
      })
    }
  }

  const handleDelete = (id: string) => {
    setStudents(students.filter((s) => s.id !== id))
    toast({
      title: "Student Deleted",
      description: "The student has been removed from the system.",
      variant: "destructive",
    })
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Student Accounts</CardTitle>
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search students..."
              className="w-[200px] pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
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
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Student ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Password</TableHead>
              <TableHead>Email</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredStudents.map((student) => (
              <TableRow key={student.id}>
                <TableCell className="font-medium">{student.id}</TableCell>
                <TableCell>{student.name}</TableCell>
                <TableCell>{student.password}</TableCell>
                <TableCell>{student.email}</TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-2">
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button variant="outline" size="icon" onClick={() => handleEdit(student)}>
                          <Edit className="h-4 w-4" />
                        </Button>
                      </DialogTrigger>
                      <DialogContent>
                        <DialogHeader>
                          <DialogTitle>Edit Student</DialogTitle>
                        </DialogHeader>
                        {editingStudent && (
                          <div className="grid gap-4 py-4">
                            <div className="grid gap-2">
                              <label htmlFor="id">Student ID</label>
                              <Input
                                id="id"
                                value={editingStudent.id}
                                onChange={(e) => setEditingStudent({ ...editingStudent, id: e.target.value })}
                                readOnly
                              />
                            </div>
                            <div className="grid gap-2">
                              <label htmlFor="name">Name</label>
                              <Input
                                id="name"
                                value={editingStudent.name}
                                onChange={(e) => setEditingStudent({ ...editingStudent, name: e.target.value })}
                              />
                            </div>
                            <div className="grid gap-2">
                              <label htmlFor="password">Password</label>
                              <Input
                                id="password"
                                value={editingStudent.password}
                                onChange={(e) => setEditingStudent({ ...editingStudent, password: e.target.value })}
                              />
                            </div>
                            <div className="grid gap-2">
                              <label htmlFor="email">Email</label>
                              <Input
                                id="email"
                                value={editingStudent.email}
                                onChange={(e) => setEditingStudent({ ...editingStudent, email: e.target.value })}
                              />
                            </div>
                            <div className="flex justify-end">
                              <Button onClick={handleSaveEdit}>Save Changes</Button>
                            </div>
                          </div>
                        )}
                      </DialogContent>
                    </Dialog>
                    <Button
                      variant="outline"
                      size="icon"
                      className="text-red-500 hover:text-red-700 hover:bg-red-50"
                      onClick={() => handleDelete(student.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
