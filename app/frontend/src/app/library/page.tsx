"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { api, ApiError } from "@/lib/api"
import { useAuth } from "@/contexts/auth-context"

interface Document {
  id: string
  owner_id: string
  title: string
  filename: string
  format: string
  size: number
  status: string
  created_at: string
  updated_at: string
}

export default function LibraryPage() {
  const { token } = useAuth()
  const router = useRouter()
  const [documents, setDocuments] = useState<Document[]>([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [searchQuery, setSearchQuery] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const perPage = 20

  useEffect(() => {
    if (!token) {
      router.push("/login")
      return
    }
    fetchDocuments()
  }, [page, searchQuery, token])

  async function fetchDocuments() {
    setLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams({
        page: String(page),
        per_page: String(perPage),
      })
      if (searchQuery) {
        params.append("q", searchQuery)
      }

      const data = await api.get<{ documents: Document[]; total: number }>(
        `/document/list?${params}`,
      )
      setDocuments(data.documents)
      setTotal(data.total)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to fetch documents")
    } finally {
      setLoading(false)
    }
  }

  async function deleteDocument(id: string) {
    if (!confirm("Are you sure you want to delete this document?")) return
    try {
      await api.delete(`/document/delete/${id}`)
      setDocuments((prev) => prev.filter((doc) => doc.id !== id))
      setTotal((prev) => prev - 1)
    } catch (err) {
      alert(err instanceof ApiError ? err.message : "Failed to delete document")
    }
  }

  function formatFileSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  const totalPages = Math.ceil(total / perPage)

  return (
    <>
      <div className="mb-6 flex items-center justify-between">
        <input
          type="text"
          placeholder="Search documents..."
          value={searchQuery}
          onChange={(e) => {
            setSearchQuery(e.target.value)
            setPage(1)
          }}
          className="w-full max-w-md px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <Link
          href="/library/upload"
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
        >
          Upload Document
        </Link>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      ) : documents.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">No documents found</p>
          <Link
            href="/library/upload"
            className="text-blue-600 hover:text-blue-800"
          >
            Upload your first document
          </Link>
        </div>
      ) : (
        <>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50 border-b">
                  <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Title</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Format</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Size</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Status</th>
                  <th className="text-left px-4 py-3 text-sm font-medium text-gray-600">Uploaded</th>
                  <th className="text-right px-4 py-3 text-sm font-medium text-gray-600">Actions</th>
                </tr>
              </thead>
              <tbody>
                {documents.map((doc) => (
                  <tr key={doc.id} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{doc.title}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{doc.format}</td>
                    <td className="px-4 py-3 text-sm text-gray-600">{formatFileSize(doc.size)}</td>
                    <td className="px-4 py-3">
                      <span
                        className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                          doc.status === "uploaded"
                            ? "bg-green-100 text-green-800"
                            : doc.status === "upload_failed"
                              ? "bg-red-100 text-red-800"
                              : "bg-yellow-100 text-yellow-800"
                        }`}
                      >
                        {doc.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600">
                      {new Date(doc.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-3 text-right">
                      <button
                        onClick={() => deleteDocument(doc.id)}
                        className="text-sm text-red-600 hover:text-red-800"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-600">
                Showing {(page - 1) * perPage + 1}-{Math.min(page * perPage, total)} of {total}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                  disabled={page === 1}
                  className="px-3 py-1 text-sm border rounded-md disabled:opacity-50 hover:bg-gray-100"
                >
                  Previous
                </button>
                <button
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                  disabled={page === totalPages}
                  className="px-3 py-1 text-sm border rounded-md disabled:opacity-50 hover:bg-gray-100"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </>
  )
}
