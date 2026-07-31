"use client"

import { useState, useRef, useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/auth-context"
import { api, ApiError } from "@/lib/api"

interface Message {
  id: string
  role: "user" | "agent"
  content: string
  timestamp: Date
  agentType?: string
  runId?: string
  durationMs?: number
}

export default function ChatPage() {
  const { token } = useAuth()
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "agent",
      content: "Hello! I can help you work with your documents. Try asking me to summarize, create a quiz, or translate content.",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [documentId, setDocumentId] = useState("")
  const [loading, setLoading] = useState(false)
  const [agentType, setAgentType] = useState("echo")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    if (!token) router.push("/login")
  }, [token, router])

  async function handleSend() {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const envelope = {
        document_id: documentId || "chat-doc",
        node_ids: [],
        agent_params: { query: userMessage.content },
        trace_id: crypto.randomUUID(),
      }
      const result = await api.post<{
        run_id: string
        response: { status: string; output: Record<string, unknown>; error?: { code: string; message: string } | null }
        duration_ms: number
      }>(`/agents/${agentType}/invoke`, envelope)

      const agentMessage: Message = {
        id: result.run_id,
        role: "agent",
        content: result.response.output
          ? JSON.stringify(result.response.output, null, 2)
          : result.response.error?.message || "No response",
        timestamp: new Date(),
        agentType,
        runId: result.run_id,
        durationMs: result.duration_ms,
      }
      setMessages((prev) => [...prev, agentMessage])
    } catch (err) {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "agent",
        content: err instanceof ApiError ? err.message : "Agent invocation failed",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      <div className="mb-4 flex items-center gap-4 flex-wrap">
        <h1 className="text-2xl font-bold text-gray-900">Chat</h1>
        <input
          type="text"
          value={documentId}
          onChange={(e) => setDocumentId(e.target.value)}
          placeholder="Document ID (optional)"
          className="px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={agentType}
          onChange={(e) => setAgentType(e.target.value)}
          className="px-3 py-1.5 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="echo">Echo Agent</option>
          <option value="summary">Summary Agent</option>
          <option value="quiz">Quiz Agent</option>
          <option value="translation">Translation Agent</option>
          <option value="diagram">Diagram Agent</option>
          <option value="revision">Revision Agent</option>
          <option value="recommendation">Recommendation Agent</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto bg-white rounded-lg shadow p-4 mb-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-100 text-gray-900"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              {msg.durationMs && (
                <p className="text-xs mt-1 opacity-60">{msg.durationMs}ms</p>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-2">
              <p className="text-sm text-gray-500">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type a message..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSend}
          disabled={loading || !input.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  )
}
