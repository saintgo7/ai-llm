import React from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import {
  LayoutDashboard,
  CheckSquare,
  MessageSquare,
  FileText,
  LogOut,
  Menu,
} from 'lucide-react'

function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { to: '/tasks', icon: CheckSquare, label: '작업 관리' },
    { to: '/chat', icon: MessageSquare, label: '실시간 채팅' },
    { to: '/dashboard', icon: LayoutDashboard, label: '대시보드' },
    { to: '/api-docs', icon: FileText, label: 'API 문서' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-primary-600">AI-LLM</h1>
              </div>
            </div>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex space-x-4">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) =>
                      `flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                      }`
                    }
                  >
                    <Icon className="w-4 h-4 mr-2" />
                    {item.label}
                  </NavLink>
                )
              })}
            </nav>

            {/* User Menu */}
            <div className="hidden md:flex items-center space-x-4">
              {user && (
                <span className="text-sm text-gray-600">
                  {user.username || user.email}
                </span>
              )}
              <button
                onClick={handleLogout}
                className="flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
              >
                <LogOut className="w-4 h-4 mr-2" />
                로그아웃
              </button>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-md text-gray-600 hover:bg-gray-100"
              >
                <Menu className="w-6 h-6" />
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    onClick={() => setMobileMenuOpen(false)}
                    className={({ isActive }) =>
                      `flex items-center px-3 py-2 rounded-md text-base font-medium ${
                        isActive
                          ? 'bg-primary-100 text-primary-700'
                          : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'
                      }`
                    }
                  >
                    <Icon className="w-5 h-5 mr-3" />
                    {item.label}
                  </NavLink>
                )
              })}
              <button
                onClick={handleLogout}
                className="w-full flex items-center px-3 py-2 rounded-md text-base font-medium text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              >
                <LogOut className="w-5 h-5 mr-3" />
                로그아웃
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-500">
              © 2025 AI-LLM. All rights reserved.
            </p>
            <div className="flex space-x-4">
              <a
                href="/api-docs"
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                API 문서
              </a>
              <a
                href="http://localhost:3000"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Grafana
              </a>
              <a
                href="http://localhost:9090"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-500 hover:text-gray-700"
              >
                Prometheus
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout
