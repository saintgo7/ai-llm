import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { authApi } from '../lib/api'
import toast from 'react-hot-toast'
import { Lock, User } from 'lucide-react'

function Login() {
  const navigate = useNavigate()
  const login = useAuthStore((state) => state.login)
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await authApi.login(credentials)
      const { token, user } = response.data

      login(user, token)
      toast.success('로그인 성공!')
      navigate('/tasks')
    } catch (error) {
      console.error('Login error:', error)
      toast.error(
        error.response?.data?.message || '로그인 실패. 다시 시도해주세요.'
      )
    } finally {
      setLoading(false)
    }
  }

  const handleDemoLogin = () => {
    setCredentials({
      username: 'admin',
      password: 'admin123',
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        {/* Logo and Title */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">AI-LLM</h1>
          <p className="text-primary-100">
            작업 관리 및 실시간 협업 플랫폼
          </p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">로그인</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username */}
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                사용자명
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <User className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="username"
                  type="text"
                  value={credentials.username}
                  onChange={(e) =>
                    setCredentials({ ...credentials, username: e.target.value })
                  }
                  className="input pl-10"
                  placeholder="admin"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                비밀번호
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  type="password"
                  value={credentials.password}
                  onChange={(e) =>
                    setCredentials({ ...credentials, password: e.target.value })
                  }
                  className="input pl-10"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary w-full"
            >
              {loading ? '로그인 중...' : '로그인'}
            </button>
          </form>

          {/* Demo Login */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <button
              onClick={handleDemoLogin}
              className="btn btn-secondary w-full"
            >
              데모 계정으로 로그인
            </button>
            <p className="text-xs text-gray-500 text-center mt-2">
              데모 계정: admin / admin123
            </p>
          </div>
        </div>

        {/* Features */}
        <div className="mt-8 grid grid-cols-3 gap-4 text-center">
          <div className="text-white">
            <div className="text-2xl font-bold">50+</div>
            <div className="text-sm text-primary-100">프로그램</div>
          </div>
          <div className="text-white">
            <div className="text-2xl font-bold">13</div>
            <div className="text-sm text-primary-100">서비스</div>
          </div>
          <div className="text-white">
            <div className="text-2xl font-bold">100%</div>
            <div className="text-sm text-primary-100">테스트</div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
