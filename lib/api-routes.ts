// This file outlines the API routes needed for the backend

export const apiRoutes = {
  // Authentication
  auth: {
    login: "/api/auth/login",
    logout: "/api/auth/logout",
    session: "/api/auth/session",
  },

  // Users
  users: {
    getAll: "/api/users",
    getById: (id: string) => `/api/users/${id}`,
    create: "/api/users",
    update: (id: string) => `/api/users/${id}`,
    delete: (id: string) => `/api/users/${id}`,
  },

  // Courses
  courses: {
    getAll: "/api/courses",
    getById: (id: string) => `/api/courses/${id}`,
    create: "/api/courses",
    update: (id: string) => `/api/courses/${id}`,
    delete: (id: string) => `/api/courses/${id}`,
    getStudents: (id: string) => `/api/courses/${id}/students`,
    addStudent: (id: string) => `/api/courses/${id}/students`,
    removeStudent: (id: string, studentId: string) => `/api/courses/${id}/students/${studentId}`,
  },

  // Assignments
  assignments: {
    getAll: "/api/assignments",
    getByCourse: (courseId: string) => `/api/courses/${courseId}/assignments`,
    getById: (id: string) => `/api/assignments/${id}`,
    create: "/api/assignments",
    update: (id: string) => `/api/assignments/${id}`,
    delete: (id: string) => `/api/assignments/${id}`,
    getQuestions: (id: string) => `/api/assignments/${id}/questions`,
  },

  // Submissions
  submissions: {
    getByAssignment: (assignmentId: string) => `/api/assignments/${assignmentId}/submissions`,
    getByStudent: (studentId: string) => `/api/students/${studentId}/submissions`,
    getById: (id: string) => `/api/submissions/${id}`,
    create: "/api/submissions",
    update: (id: string) => `/api/submissions/${id}`,
    grade: (id: string) => `/api/submissions/${id}/grade`,
  },
}
