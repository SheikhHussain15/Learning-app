"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/auth-context"
import { api, ApiError } from "@/lib/api"

interface EchoResponse {
  status: string
  run_id: string
  response: {
    status: string
    output: {
      echoed_document_id: string
      echoed_node_ids: string[]
      echoed_trace_id: string
      received_agent_params: Record<string, unknown>
    }
    source_refs: string[]
    usage: { prompt_tokens: number; completion_tokens: number; total_tokens: number }
    error: { code: string; message: string; retryable: boolean } | null
  }
  duration_ms: number
}

const agentTypes = [
  { value: "echo", label: "Echo Agent", desc: "Validates infrastructure" },
  { value: "summary", label: "Summary Agent", desc: "Summarizes documents" },
  { value: "quiz", label: "Quiz Agent", desc: "Generates quiz questions" },
  { value: "translation", label: "Translation Agent", desc: "Translates content" },
  { value: "diagram", label: "Diagram Agent", desc: "Creates diagrams" },
  { value: "revision", label: "Revision Agent", desc: "Spaced repetition review" },
  { value: "recommendation", label: "Recommendation Agent", desc: "Suggests next content" },
]

export default function AgentsPage() {
  const { token } = useAuth()
  const router = useRouter()
  const [agentType, setAgentType] = useState("echo")

  useEffect(() => {
    if (!token) router.push("/login")
  }, [token, router])
  const [documentId, setDocumentId] = useState("")
  const [nodeIds, setNodeIds] = useState("")
  const [result, setResult] = useState<EchoResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function handleInvoke() {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await api.post<EchoResponse>(`/agents/${agentType}/invoke`, {
        document_id: documentId || "test-doc-1",
        node_ids: nodeIds ? nodeIds.split(",").map((s) => s.trim()) : [],
        agent_params: { test: true },
        trace_id: crypto.randomUUID(),
      })
      setResult(data)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Invocation failed")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">AI Agents</h1>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Agent Type</label>
            <select
              value={agentType}
              onChange={(e) => setAgentType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {agentTypes.map((at) => (
                <option key={at.value} value={at.value}>
                  {at.label}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              {agentTypes.find((at) => at.value === agentType)?.desc}
            </p>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Document ID</label>
            <input
              type="text"
              value={documentId}
              onChange={(e) => setDocumentId(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="doc-123"
            />
          </div>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Node IDs (comma-separated)
          </label>
          <input
            type="text"
            value={nodeIds}
            onChange={(e) => setNodeIds(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="node-1, node-2"
          />
        </div>

        <button
          onClick={handleInvoke}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Invoking..." : "Invoke Agent"}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Response</h2>
          <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
            <div>
              <span className="font-medium text-gray-600">Status:</span>{" "}
              <span
                className={
                  result.response.status === "success" ? "text-green-600" : "text-red-600"
                }
              >
                {result.response.status}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-600">Duration:</span>{" "}
              {result.duration_ms}ms
            </div>
            <div>
              <span className="font-medium text-gray-600">Run ID:</span>{" "}
              <span className="font-mono text-xs">{result.run_id}</span>
            </div>
            <div>
              <span className="font-medium text-gray-600">Tokens:</span>{" "}
              {result.response.usage.total_tokens} (P:{result.response.usage.prompt_tokens} C:{result.response.usage.completion_tokens})
            </div>
          </div>

          {result.response.error && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm mb-4">
              <strong>Error:</strong> {result.response.error.code} — {result.response.error.message}
            </div>
          )}

          {result.response.output && Object.keys(result.response.output).length > 0 && (
            <div>
              <h3 className="text-sm font-medium text-gray-600 mb-2">Output</h3>
              <pre className="bg-gray-50 p-4 rounded-md text-sm overflow-auto max-h-96">
                {JSON.stringify(result.response.output, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
