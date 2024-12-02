"use client"
import { RegistrationProvider } from "./context/registration-context"

export default function Register({ children }: { children: React.ReactNode }) {

  return (
    <RegistrationProvider>
      <div className="bg-gray-100 min-h-screen">
        {children}
      </div>
    </RegistrationProvider>
  )
}

