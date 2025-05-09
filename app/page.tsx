import { LoginForm } from "@/components/login-form"

export default function Home() {
  return (
    <main className="min-h-screen flex items-center justify-center bg-gradient-to-br from-amber-50 to-orange-100">
      <div className="w-full max-w-md">
        <LoginForm />
      </div>
    </main>
  )
}
