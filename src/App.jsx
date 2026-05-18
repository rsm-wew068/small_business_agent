import { useState, useRef, useEffect } from 'react'
import ChatWindow from './components/ChatWindow'
import ChatInput from './components/ChatInput'
import QuickActions from './components/QuickActions'
import AdminPanel from './components/AdminPanel'

const STORAGE_KEY = 'erics-auto-care-messages'
const SESSION_KEY = 'erics-auto-care-session'

function getSessionId() {
  let id = localStorage.getItem(SESSION_KEY)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(SESSION_KEY, id)
  }
  return id
}

const WELCOME_MESSAGE = {
  role: 'assistant',
  content: "Welcome to Eric's Auto Care! 🔧 I'm your virtual assistant. I can help you with our services, book an appointment, or answer any questions. How can I help you today?"
}

function loadMessages() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) return JSON.parse(saved)
  } catch {}
  return [WELCOME_MESSAGE]
}

export default function App() {
  const [messages, setMessages] = useState(loadMessages)
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState('chat')
  const bottomRef = useRef(null)

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages))
  }, [messages])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text) => {
    if (!text.trim() || loading) return

    const userMessage = { role: 'user', content: text }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setLoading(true)

    try {
      const history = newMessages.filter(m => m.role !== 'tool')
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history, session_id: getSessionId() }),
      })

      if (!res.ok) throw new Error('Request failed')

      const data = await res.json()
      setMessages([...newMessages, { role: 'assistant', content: data.response }])
    } catch {
      setMessages([...newMessages, {
        role: 'assistant',
        content: "I'm sorry, something went wrong. Please try again or call us at (555) 842-3678."
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleNewChat = () => {
    setMessages([WELCOME_MESSAGE])
  }

  if (page === 'admin') {
    return <AdminPanel onBack={() => setPage('chat')} />
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between shadow-sm">
        <div className="flex items-center gap-3">
          <span className="text-2xl">🔧</span>
          <div>
            <h1 className="text-lg font-semibold text-gray-900 leading-tight">Eric's Auto Care</h1>
            <p className="text-xs text-gray-500 hidden sm:block">Your Trusted Neighborhood Auto Shop</p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setPage('admin')}
            className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-100 transition-colors"
          >
            Admin
          </button>
          <button
            onClick={handleNewChat}
            className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-100 transition-colors"
          >
            + New Chat
          </button>
        </div>
      </header>

      <ChatWindow messages={messages} loading={loading} bottomRef={bottomRef} />

      {messages.length <= 1 && !loading && (
        <QuickActions onSelect={sendMessage} />
      )}

      <ChatInput onSend={sendMessage} loading={loading} />
    </div>
  )
}
