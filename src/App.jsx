import { useState, useRef, useEffect } from 'react'
import ChatWindow from './components/ChatWindow'
import ChatInput from './components/ChatInput'
import QuickActions from './components/QuickActions'

const WELCOME_MESSAGE = {
  role: 'assistant',
  content: "Welcome to Eric's Auto Care! 🔧 I'm your virtual assistant. I can help you with our services, book an appointment, or answer any questions. How can I help you today?"
}

export default function App() {
  const [messages, setMessages] = useState([WELCOME_MESSAGE])
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

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
        body: JSON.stringify({ messages: history }),
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
        <button
          onClick={handleNewChat}
          className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-100 transition-colors"
        >
          + New Chat
        </button>
      </header>

      <ChatWindow messages={messages} loading={loading} bottomRef={bottomRef} />

      {messages.length <= 1 && !loading && (
        <QuickActions onSelect={sendMessage} />
      )}

      <ChatInput onSend={sendMessage} loading={loading} />
    </div>
  )
}
