"use client"

import type React from "react"

import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { LayoutDashboard, Users, FileText, BookOpen, UserPlus, LogOut } from "lucide-react"
import { cn } from "@/lib/utils"

interface NavItem {
  title: string
  href: string
  icon: React.ReactNode
}

export function TeacherSidebar() {
  const pathname = usePathname()
  const router = useRouter()

  const navItems: NavItem[] = [
    {
      title: "Dashboard",
      href: "/dashboard/teacher",
      icon: <LayoutDashboard className="mr-2 h-4 w-4" />,
    },
    {
      title: "Students",
      href: "/dashboard/teacher/students",
      icon: <Users className="mr-2 h-4 w-4" />,
    },
    {
      title: "Assignments",
      href: "/dashboard/teacher/assignments",
      icon: <FileText className="mr-2 h-4 w-4" />,
    },
    {
      title: "Courses",
      href: "/dashboard/teacher/courses",
      icon: <BookOpen className="mr-2 h-4 w-4" />,
    },
    {
      title: "Register New",
      href: "/dashboard/teacher/register",
      icon: <UserPlus className="mr-2 h-4 w-4" />,
    },
  ]

  const handleLogout = () => {
    // In a real app, you would handle logout logic here
    router.push("/")
  }

  return (
    <div className="hidden border-r bg-white lg:block lg:w-64">
      <div className="flex h-full flex-col">
        <div className="flex h-14 items-center border-b px-4">
          <Link href="/dashboard/teacher" className="flex items-center font-semibold">
            <BookOpen className="mr-2 h-5 w-5 text-orange-500" />
            <span>Grading System</span>
          </Link>
        </div>
        <ScrollArea className="flex-1 py-4">
          <nav className="grid gap-1 px-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center rounded-md px-3 py-2 text-sm font-medium hover:bg-gray-100",
                  pathname === item.href ? "bg-gray-100" : "transparent",
                )}
              >
                {item.icon}
                {item.title}
              </Link>
            ))}
          </nav>
        </ScrollArea>
        <div className="border-t p-4">
          <Button
            variant="outline"
            className="w-full justify-start text-red-500 hover:text-red-600 hover:bg-red-50"
            onClick={handleLogout}
          >
            <LogOut className="mr-2 h-4 w-4" />
            Log Out
          </Button>
        </div>
      </div>
    </div>
  )
}
