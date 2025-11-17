import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { taskApi } from '../lib/api'
import toast from 'react-hot-toast'
import {
  Plus,
  Edit2,
  Trash2,
  CheckCircle,
  Circle,
  Search,
  Filter,
} from 'lucide-react'
import { format } from 'date-fns'

function TaskManager() {
  const queryClient = useQueryClient()
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all') // all, completed, pending
  const [formData, setFormData] = useState({
    title: '',
    description: '',
  })

  // Fetch tasks
  const { data: tasks, isLoading } = useQuery('tasks', async () => {
    const response = await taskApi.getAll()
    return response.data
  })

  // Create task mutation
  const createMutation = useMutation(taskApi.create, {
    onSuccess: () => {
      queryClient.invalidateQueries('tasks')
      toast.success('작업이 생성되었습니다')
      closeModal()
    },
    onError: (error) => {
      toast.error(error.response?.data?.message || '작업 생성 실패')
    },
  })

  // Update task mutation
  const updateMutation = useMutation(
    ({ id, data }) => taskApi.update(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks')
        toast.success('작업이 업데이트되었습니다')
        closeModal()
      },
      onError: (error) => {
        toast.error(error.response?.data?.message || '작업 업데이트 실패')
      },
    }
  )

  // Delete task mutation
  const deleteMutation = useMutation(taskApi.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('tasks')
      toast.success('작업이 삭제되었습니다')
    },
    onError: (error) => {
      toast.error(error.response?.data?.message || '작업 삭제 실패')
    },
  })

  // Toggle task completion
  const toggleMutation = useMutation(
    ({ id, completed }) => taskApi.update(id, { completed: !completed }),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('tasks')
      },
      onError: (error) => {
        toast.error(error.response?.data?.message || '작업 상태 변경 실패')
      },
    }
  )

  const openModal = (task = null) => {
    if (task) {
      setEditingTask(task)
      setFormData({
        title: task.title,
        description: task.description || '',
      })
    } else {
      setEditingTask(null)
      setFormData({ title: '', description: '' })
    }
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setEditingTask(null)
    setFormData({ title: '', description: '' })
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!formData.title.trim()) {
      toast.error('제목을 입력해주세요')
      return
    }

    if (editingTask) {
      updateMutation.mutate({ id: editingTask.id, data: formData })
    } else {
      createMutation.mutate(formData)
    }
  }

  const handleDelete = (id) => {
    if (window.confirm('정말 이 작업을 삭제하시겠습니까?')) {
      deleteMutation.mutate(id)
    }
  }

  const handleToggle = (task) => {
    toggleMutation.mutate({ id: task.id, completed: task.completed })
  }

  // Filter and search tasks
  const filteredTasks = tasks?.filter((task) => {
    const matchesSearch = task.title
      .toLowerCase()
      .includes(searchTerm.toLowerCase())
    const matchesFilter =
      filterStatus === 'all' ||
      (filterStatus === 'completed' && task.completed) ||
      (filterStatus === 'pending' && !task.completed)

    return matchesSearch && matchesFilter
  })

  const stats = {
    total: tasks?.length || 0,
    completed: tasks?.filter((t) => t.completed).length || 0,
    pending: tasks?.filter((t) => !t.completed).length || 0,
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">작업 관리</h1>
          <p className="text-gray-600 mt-1">
            할 일 목록을 생성하고 관리하세요
          </p>
        </div>
        <button onClick={() => openModal()} className="btn btn-primary">
          <Plus className="w-5 h-5 mr-2" />
          새 작업 추가
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">전체 작업</p>
              <p className="text-3xl font-bold text-blue-700">{stats.total}</p>
            </div>
            <Circle className="w-12 h-12 text-blue-400" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-50 to-green-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">완료된 작업</p>
              <p className="text-3xl font-bold text-green-700">
                {stats.completed}
              </p>
            </div>
            <CheckCircle className="w-12 h-12 text-green-400" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-yellow-50 to-yellow-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">대기 중</p>
              <p className="text-3xl font-bold text-yellow-700">
                {stats.pending}
              </p>
            </div>
            <Circle className="w-12 h-12 text-yellow-400" />
          </div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="card">
        <div className="flex flex-col md:flex-row gap-4">
          {/* Search */}
          <div className="flex-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="작업 검색..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input pl-10"
            />
          </div>

          {/* Filter */}
          <div className="flex items-center gap-2">
            <Filter className="h-5 w-5 text-gray-400" />
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="input"
            >
              <option value="all">전체</option>
              <option value="pending">대기 중</option>
              <option value="completed">완료</option>
            </select>
          </div>
        </div>
      </div>

      {/* Task List */}
      <div className="card">
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">작업 목록을 불러오는 중...</p>
          </div>
        ) : filteredTasks?.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">작업이 없습니다</p>
            <button
              onClick={() => openModal()}
              className="btn btn-primary mt-4"
            >
              첫 작업 추가하기
            </button>
          </div>
        ) : (
          <div className="space-y-2">
            {filteredTasks?.map((task) => (
              <div
                key={task.id}
                className={`flex items-center gap-4 p-4 rounded-lg border transition-colors ${
                  task.completed
                    ? 'bg-gray-50 border-gray-200'
                    : 'bg-white border-gray-300 hover:border-primary-300'
                }`}
              >
                {/* Checkbox */}
                <button
                  onClick={() => handleToggle(task)}
                  className="flex-shrink-0"
                >
                  {task.completed ? (
                    <CheckCircle className="w-6 h-6 text-green-500" />
                  ) : (
                    <Circle className="w-6 h-6 text-gray-400 hover:text-primary-500" />
                  )}
                </button>

                {/* Task Info */}
                <div className="flex-1 min-w-0">
                  <h3
                    className={`font-medium ${
                      task.completed
                        ? 'line-through text-gray-500'
                        : 'text-gray-900'
                    }`}
                  >
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className="text-sm text-gray-600 mt-1">
                      {task.description}
                    </p>
                  )}
                  <p className="text-xs text-gray-400 mt-1">
                    생성일:{' '}
                    {task.created_at
                      ? format(new Date(task.created_at), 'yyyy-MM-dd HH:mm')
                      : 'N/A'}
                  </p>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => openModal(task)}
                    className="p-2 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                  >
                    <Edit2 className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(task.id)}
                    className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              {editingTask ? '작업 수정' : '새 작업 추가'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Title */}
              <div>
                <label
                  htmlFor="title"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  제목 *
                </label>
                <input
                  id="title"
                  type="text"
                  value={formData.title}
                  onChange={(e) =>
                    setFormData({ ...formData, title: e.target.value })
                  }
                  className="input"
                  placeholder="작업 제목을 입력하세요"
                  required
                />
              </div>

              {/* Description */}
              <div>
                <label
                  htmlFor="description"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  설명
                </label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) =>
                    setFormData({ ...formData, description: e.target.value })
                  }
                  className="input min-h-[100px]"
                  placeholder="작업 설명을 입력하세요 (선택사항)"
                  rows={4}
                />
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-4">
                <button type="submit" className="btn btn-primary flex-1">
                  {editingTask ? '수정' : '생성'}
                </button>
                <button
                  type="button"
                  onClick={closeModal}
                  className="btn btn-secondary flex-1"
                >
                  취소
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default TaskManager
