import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

// Mock data for recent activity
const activities = [
  {
    id: 1,
    user: {
      name: "Rishika snehi",
      image: "/placeholder-user.jpg",
      initials: "RS",
    },
    action: "submitted",
    target: "Final Project",
    time: "2 hours ago",
  },
  {
    id: 2,
    user: {
      name: "Sarika",
      image: "/placeholder-user.jpg",
      initials: "sk",
    },
    action: "submitted",
    target: "DBMS assignment",
    time: "5 hours ago",
  },
  {
    id: 3,
    user: {
      name: "Likita MG",
      image: "/placeholder-user.jpg",
      initials: "LMG",
    },
    action: "registered",
    target: "CS108",
    time: "1 day ago",
  },
  {
    id: 4,
    user: {
      name: "Saksham Upadhya",
      image: "/placeholder-user.jpg",
      initials: "Su",
    },
    action: "created",
    target: "UHV placards submitted",
    time: "2 days ago",
  },
  {
    id: 5,
    user: {
      name: "Shreya S",
      image: "/placeholder-user.jpg",
      initials: "SS",
    },
    action: "submitted",
    target: "DBMS project submitted",
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
