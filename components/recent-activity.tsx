import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

// Mock data for recent activity
const activities = [
  {
    id: 1,
    user: {
      name: "Kennard Wang",
      image: "/placeholder-user.jpg",
      initials: "KW",
    },
    action: "submitted",
    target: "Final Project",
    time: "2 hours ago",
  },
  {
    id: 2,
    user: {
      name: "Cyx",
      image: "/placeholder-user.jpg",
      initials: "CX",
    },
    action: "submitted",
    target: "Assignment 2",
    time: "5 hours ago",
  },
  {
    id: 3,
    user: {
      name: "Kiera Yi",
      image: "/placeholder-user.jpg",
      initials: "KY",
    },
    action: "registered",
    target: "CS108",
    time: "1 day ago",
  },
  {
    id: 4,
    user: {
      name: "Kenneth Lo",
      image: "/placeholder-user.jpg",
      initials: "KL",
    },
    action: "created",
    target: "Assignment 2",
    time: "2 days ago",
  },
  {
    id: 5,
    user: {
      name: "Kennard Wang",
      image: "/placeholder-user.jpg",
      initials: "KW",
    },
    action: "submitted",
    target: "Assignment 1",
    time: "3 days ago",
  },
]

export function RecentActivity() {
  return (
    <div className="space-y-4">
      {activities.map((activity) => (
        <div key={activity.id} className="flex items-center gap-4">
          <Avatar className="h-8 w-8">
            <AvatarImage src={activity.user.image || "/placeholder.svg"} alt={activity.user.name} />
            <AvatarFallback>{activity.user.initials}</AvatarFallback>
          </Avatar>
          <div className="space-y-1">
            <p className="text-sm font-medium leading-none">
              {activity.user.name}{" "}
              <span className="text-muted-foreground">
                {activity.action} {activity.target}
              </span>
            </p>
            <p className="text-xs text-muted-foreground">{activity.time}</p>
          </div>
        </div>
      ))}
    </div>
  )
}
