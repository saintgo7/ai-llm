import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import TaskManager from './pages/TaskManager'
import Chat from './pages/Chat'
import Dashboard from './pages/Dashboard'
import ApiDocs from './pages/ApiDocs'
import Login from './pages/Login'
import { useAuthStore } from './store/authStore'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<Layout />}>
        <Route path="/" element={<Navigate to="/tasks" replace />} />
        <Route
          path="/tasks"
          element={isAuthenticated ? <TaskManager /> : <Navigate to="/login" />}
        />
        <Route
          path="/chat"
          element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route path="/api-docs" element={<ApiDocs />} />
      </Route>
    </Routes>
  )
}

export default App
