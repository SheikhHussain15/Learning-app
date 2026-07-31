import Link from "next/link"

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100">
      <h1 className="text-4xl font-bold mb-4">AI Learning Platform</h1>
      <p className="text-gray-600 mb-8">Your journey to learn with AI starts here</p>
      <div className="flex gap-4">
        <Link
          href="/login"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          Login
        </Link>
        <Link
          href="/register"
          className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-100"
        >
          Register
        </Link>
      </div>
    </div>
  )
}