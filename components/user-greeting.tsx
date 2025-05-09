import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

interface UserGreetingProps {
  name: string
  role: string
}

export function UserGreeting({ name, role }: UserGreetingProps) {
  // Get current time to display appropriate greeting
  const currentHour = new Date().getHours()
  let greeting = "Good evening"

  if (currentHour < 12) {
    greeting = "Good morning"
  } else if (currentHour < 18) {
    greeting = "Good afternoon"
  }

  // Get initials for avatar fallback
  const initials = name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()

  return (
    <div className="flex items-center justify-between">
      <div className="space-y-1">
        <h2 className="text-3xl font-bold tracking-tight">
          {greeting}, {name}
        </h2>
        <p className="text-muted-foreground">Welcome to your {role.toLowerCase()} dashboard</p>
      </div>
      <Avatar className="h-12 w-12">
        <AvatarImage src="/placeholder-user.jpg" alt={name} />
        <AvatarFallback>{initials}</AvatarFallback>
      </Avatar>
    </div>
  )
}
