import React, { useState, useEffect, useRef } from 'react'
import { io } from 'socket.io-client'
import { useAuthStore } from '../store/authStore'
import toast from 'react-hot-toast'
import {
  Send,
  Users,
  MessageSquare,
  AlertCircle,
  CheckCircle,
} from 'lucide-react'
import { format } from 'date-fns'

function Chat() {
  const { user } = useAuthStore()
  const [socket, setSocket] = useState(null)
  const [connected, setConnected] = useState(false)
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [username, setUsername] = useState(user?.username || 'Anonymous')
  const [room, setRoom] = useState('general')
  const [usernameSet, setUsernameSet] = useState(false)
  const [activeUsers, setActiveUsers] = useState(0)
  const messagesEndRef = useRef(null)

  const rooms = [
    { id: 'general', name: '일반', description: '일반 대화방' },
    { id: 'dev', name: '개발', description: '개발 관련 대화' },
    { id: 'support', name: '지원', description: '기술 지원' },
  ]

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize WebSocket connection
  useEffect(() => {
    if (!usernameSet) return

    // Connect to WebSocket server
    const newSocket = io('http://localhost:5002', {
      transports: ['websocket', 'polling'],
    })

    newSocket.on('connect', () => {
      console.log('Connected to WebSocket server')
      setConnected(true)
      toast.success('채팅 서버에 연결되었습니다')

      // Join room
      newSocket.emit('join', { username, room })
    })

    newSocket.on('disconnect', () => {
      console.log('Disconnected from WebSocket server')
      setConnected(false)
      toast.error('채팅 서버 연결이 끊어졌습니다')
    })

    newSocket.on('connect_error', (error) => {
      console.error('Connection error:', error)
      setConnected(false)
      toast.error('채팅 서버 연결 실패')
    })

    // Listen for new messages
    newSocket.on('new_message', (data) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + Math.random(),
          username: data.username,
          message: data.message,
          timestamp: data.timestamp || new Date().toISOString(),
          isOwn: data.username === username,
        },
      ])
    })

    // Listen for system messages
    newSocket.on('system_message', (data) => {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + Math.random(),
          message: data.message,
          timestamp: data.timestamp || new Date().toISOString(),
          isSystem: true,
        },
      ])
    })

    // Listen for room info
    newSocket.on('room_info', (data) => {
      setActiveUsers(data.users || 0)
    })

    setSocket(newSocket)

    return () => {
      newSocket.close()
    }
  }, [usernameSet, username, room])

  const handleSetUsername = (e) => {
    e.preventDefault()
    if (username.trim()) {
      setUsernameSet(true)
    }
  }

  const handleSendMessage = (e) => {
    e.preventDefault()

    if (!inputMessage.trim() || !socket || !connected) return

    // Emit message to server
    socket.emit('message', {
      username,
      message: inputMessage.trim(),
      room,
    })

    setInputMessage('')
  }

  const handleRoomChange = (newRoom) => {
    if (socket && connected) {
      socket.emit('leave', { username, room })
      socket.emit('join', { username, room: newRoom })
      setRoom(newRoom)
      setMessages([])
    }
  }

  // Username setup screen
  if (!usernameSet) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="card max-w-md w-full">
          <div className="text-center mb-6">
            <MessageSquare className="w-16 h-16 text-primary-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900">실시간 채팅</h2>
            <p className="text-gray-600 mt-2">
              사용자명을 입력하고 대화를 시작하세요
            </p>
          </div>

          <form onSubmit={handleSetUsername} className="space-y-4">
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                사용자명
              </label>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input"
                placeholder="닉네임을 입력하세요"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary w-full">
              채팅 시작하기
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">실시간 채팅</h1>
          <p className="text-gray-600 mt-1">
            사용자명: <span className="font-medium">{username}</span>
          </p>
        </div>

        {/* Connection Status */}
        <div className="flex items-center gap-2">
          {connected ? (
            <>
              <CheckCircle className="w-5 h-5 text-green-500" />
              <span className="text-sm text-green-600">연결됨</span>
            </>
          ) : (
            <>
              <AlertCircle className="w-5 h-5 text-red-500" />
              <span className="text-sm text-red-600">연결 끊김</span>
            </>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar - Rooms and Users */}
        <div className="lg:col-span-1 space-y-4">
          {/* Active Users */}
          <div className="card">
            <div className="flex items-center gap-2 mb-4">
              <Users className="w-5 h-5 text-primary-600" />
              <h3 className="font-semibold text-gray-900">
                활성 사용자: {activeUsers}
              </h3>
            </div>
          </div>

          {/* Rooms */}
          <div className="card">
            <h3 className="font-semibold text-gray-900 mb-4">대화방</h3>
            <div className="space-y-2">
              {rooms.map((r) => (
                <button
                  key={r.id}
                  onClick={() => handleRoomChange(r.id)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    room === r.id
                      ? 'bg-primary-100 text-primary-700 border-2 border-primary-300'
                      : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border-2 border-transparent'
                  }`}
                >
                  <div className="font-medium">{r.name}</div>
                  <div className="text-xs text-gray-600">{r.description}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Chat Area */}
        <div className="lg:col-span-3">
          <div className="card h-[600px] flex flex-col">
            {/* Room Header */}
            <div className="border-b border-gray-200 pb-4 mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                #{rooms.find((r) => r.id === room)?.name}
              </h2>
              <p className="text-sm text-gray-600">
                {rooms.find((r) => r.id === room)?.description}
              </p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 mb-4">
              {messages.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <MessageSquare className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <p>메시지가 없습니다</p>
                  <p className="text-sm mt-2">첫 메시지를 보내보세요!</p>
                </div>
              ) : (
                messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${
                      msg.isSystem
                        ? 'justify-center'
                        : msg.isOwn
                        ? 'justify-end'
                        : 'justify-start'
                    }`}
                  >
                    {msg.isSystem ? (
                      <div className="bg-gray-100 text-gray-600 px-4 py-2 rounded-full text-sm">
                        {msg.message}
                      </div>
                    ) : (
                      <div
                        className={`max-w-[70%] ${
                          msg.isOwn ? 'items-end' : 'items-start'
                        }`}
                      >
                        <div
                          className={`px-4 py-2 rounded-lg ${
                            msg.isOwn
                              ? 'bg-primary-600 text-white'
                              : 'bg-gray-100 text-gray-900'
                          }`}
                        >
                          {!msg.isOwn && (
                            <div className="text-sm font-medium mb-1">
                              {msg.username}
                            </div>
                          )}
                          <div className="break-words">{msg.message}</div>
                        </div>
                        <div
                          className={`text-xs text-gray-500 mt-1 ${
                            msg.isOwn ? 'text-right' : 'text-left'
                          }`}
                        >
                          {format(new Date(msg.timestamp), 'HH:mm')}
                        </div>
                      </div>
                    )}
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <form onSubmit={handleSendMessage} className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="메시지를 입력하세요..."
                className="input flex-1"
                disabled={!connected}
              />
              <button
                type="submit"
                disabled={!connected || !inputMessage.trim()}
                className="btn btn-primary"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Chat
