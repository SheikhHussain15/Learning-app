"use client"

import Link from "next/link"
import { useRouter, usePathname } from "next/navigation"
import { useAuth } from "@/contexts/auth-context"

const navLinks = [
  { href: "/library", label: "Library" },
  { href: "/library/upload", label: "Upload" },
  { href: "/agents", label: "Agents" },
  { href: "/chat", label: "Chat" },
  { href: "/profile", label: "Profile" },
]

export function Layout({ children }: { children: React.ReactNode }) {
  const { user, token, logout } = useAuth()
  const router = useRouter()
  const pathname = usePathname()
  const isLoggedIn = !!token

  async function handleLogout() {
    await logout()
    router.push("/login")
  }

  if (pathname === "/" || pathname === "/login" || pathname === "/register") {
    return <>{children}</>
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="text-xl font-bold text-gray-900">
            AI Learning Platform
          </Link>
          {isLoggedIn && (
            <nav className="flex items-center gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`text-sm font-medium transition-colors ${
                    pathname === link.href || pathname.startsWith(link.href + "/")
                      ? "text-blue-600"
                      : "text-gray-600 hover:text-gray-900"
                  }`}
                >
                  {link.label}
                </Link>
              ))}
              <span className="text-sm text-gray-400">{user?.email}</span>
              <button
                onClick={handleLogout}
                className="text-sm text-red-600 hover:text-red-800"
              >
                Logout
              </button>
            </nav>
          )}
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-6">{children}</main>
    </div>
  )
}
