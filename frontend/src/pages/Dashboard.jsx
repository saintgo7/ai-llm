import React, { useState, useEffect } from 'react'
import { useQuery } from 'react-query'
import axios from 'axios'
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import {
  Activity,
  Database,
  Server,
  Cpu,
  HardDrive,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock,
} from 'lucide-react'

function Dashboard() {
  const [metrics, setMetrics] = useState({
    cpu: 0,
    memory: 0,
    disk: 0,
    requests: 0,
    errors: 0,
    latency: 0,
  })

  // Fetch system metrics
  const { data: prometheusData } = useQuery(
    'metrics',
    async () => {
      const response = await axios.get('http://localhost:9090/api/v1/query', {
        params: {
          query: 'up',
        },
      })
      return response.data
    },
    {
      refetchInterval: 5000, // Refresh every 5 seconds
    }
  )

  // Simulate metrics for demo (replace with real Prometheus queries)
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics({
        cpu: Math.random() * 100,
        memory: 65 + Math.random() * 20,
        disk: 45 + Math.random() * 10,
        requests: Math.floor(Math.random() * 1000),
        errors: Math.floor(Math.random() * 10),
        latency: 50 + Math.random() * 150,
      })
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  // Sample data for charts
  const [chartData, setChartData] = useState([])

  useEffect(() => {
    // Generate initial chart data
    const initialData = Array.from({ length: 20 }, (_, i) => ({
      time: `${i}s`,
      requests: Math.floor(Math.random() * 100),
      errors: Math.floor(Math.random() * 10),
      latency: Math.floor(Math.random() * 200),
      cpu: Math.random() * 100,
      memory: Math.random() * 100,
    }))
    setChartData(initialData)

    // Update chart data periodically
    const interval = setInterval(() => {
      setChartData((prev) => {
        const newData = [...prev.slice(1)]
        newData.push({
          time: `${Date.now()}`,
          requests: Math.floor(Math.random() * 100),
          errors: Math.floor(Math.random() * 10),
          latency: Math.floor(Math.random() * 200),
          cpu: Math.random() * 100,
          memory: Math.random() * 100,
        })
        return newData
      })
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const services = [
    {
      name: 'API Server',
      status: 'healthy',
      uptime: '99.9%',
      requests: '12.4k',
    },
    {
      name: 'Auth Server',
      status: 'healthy',
      uptime: '99.8%',
      requests: '8.2k',
    },
    {
      name: 'PostgreSQL',
      status: 'healthy',
      uptime: '99.9%',
      requests: '15.3k',
    },
    { name: 'Redis', status: 'healthy', uptime: '100%', requests: '24.1k' },
    {
      name: 'Elasticsearch',
      status: 'warning',
      uptime: '98.5%',
      requests: '5.2k',
    },
    {
      name: 'WebSocket',
      status: 'healthy',
      uptime: '99.7%',
      requests: '3.8k',
    },
  ]

  const alerts = [
    {
      id: 1,
      type: 'warning',
      message: 'Elasticsearch heap usage above 80%',
      time: '5 minutes ago',
    },
    {
      id: 2,
      type: 'info',
      message: 'Database backup completed successfully',
      time: '1 hour ago',
    },
    {
      id: 3,
      type: 'success',
      message: 'All health checks passed',
      time: '2 hours ago',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">시스템 대시보드</h1>
        <p className="text-gray-600 mt-1">
          실시간 시스템 메트릭 및 서비스 상태
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">CPU 사용률</p>
              <p className="text-3xl font-bold text-blue-700">
                {metrics.cpu.toFixed(1)}%
              </p>
            </div>
            <Cpu className="w-12 h-12 text-blue-400" />
          </div>
          <div className="mt-2">
            <div className="w-full bg-blue-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${metrics.cpu}%` }}
              />
            </div>
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-50 to-green-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">메모리 사용률</p>
              <p className="text-3xl font-bold text-green-700">
                {metrics.memory.toFixed(1)}%
              </p>
            </div>
            <HardDrive className="w-12 h-12 text-green-400" />
          </div>
          <div className="mt-2">
            <div className="w-full bg-green-200 rounded-full h-2">
              <div
                className="bg-green-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${metrics.memory}%` }}
              />
            </div>
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-purple-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">요청/초</p>
              <p className="text-3xl font-bold text-purple-700">
                {metrics.requests}
              </p>
            </div>
            <TrendingUp className="w-12 h-12 text-purple-400" />
          </div>
          <p className="text-sm text-purple-600 mt-2">+12.5% from last hour</p>
        </div>

        <div className="card bg-gradient-to-br from-orange-50 to-orange-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">평균 응답시간</p>
              <p className="text-3xl font-bold text-orange-700">
                {metrics.latency.toFixed(0)}ms
              </p>
            </div>
            <Clock className="w-12 h-12 text-orange-400" />
          </div>
          <p className="text-sm text-orange-600 mt-2">-5.2% from last hour</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Request Rate Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            요청 및 오류율
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area
                type="monotone"
                dataKey="requests"
                stackId="1"
                stroke="#3b82f6"
                fill="#3b82f6"
                name="요청"
              />
              <Area
                type="monotone"
                dataKey="errors"
                stackId="2"
                stroke="#ef4444"
                fill="#ef4444"
                name="오류"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Latency Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            응답 시간 (ms)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="latency"
                stroke="#8b5cf6"
                strokeWidth={2}
                name="응답시간"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Resource Usage Chart */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            시스템 리소스
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="cpu" fill="#3b82f6" name="CPU %" />
              <Bar dataKey="memory" fill="#10b981" name="Memory %" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Service Status */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            서비스 상태
          </h3>
          <div className="space-y-3">
            {services.map((service, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  {service.status === 'healthy' ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : (
                    <AlertCircle className="w-5 h-5 text-yellow-500" />
                  )}
                  <div>
                    <p className="font-medium text-gray-900">{service.name}</p>
                    <p className="text-sm text-gray-600">
                      Uptime: {service.uptime}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium text-gray-900">
                    {service.requests}
                  </p>
                  <p className="text-xs text-gray-600">requests</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Alerts */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          최근 알림
        </h3>
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`flex items-start gap-3 p-4 rounded-lg ${
                alert.type === 'warning'
                  ? 'bg-yellow-50 border border-yellow-200'
                  : alert.type === 'success'
                  ? 'bg-green-50 border border-green-200'
                  : 'bg-blue-50 border border-blue-200'
              }`}
            >
              {alert.type === 'warning' ? (
                <AlertCircle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
              ) : alert.type === 'success' ? (
                <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              ) : (
                <Activity className="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" />
              )}
              <div className="flex-1">
                <p
                  className={`font-medium ${
                    alert.type === 'warning'
                      ? 'text-yellow-900'
                      : alert.type === 'success'
                      ? 'text-green-900'
                      : 'text-blue-900'
                  }`}
                >
                  {alert.message}
                </p>
                <p className="text-sm text-gray-600 mt-1">{alert.time}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <a
          href="http://localhost:3000"
          target="_blank"
          rel="noopener noreferrer"
          className="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div className="flex items-center gap-4">
            <div className="p-3 bg-orange-100 rounded-lg">
              <Server className="w-8 h-8 text-orange-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">Grafana</h4>
              <p className="text-sm text-gray-600">고급 메트릭 대시보드</p>
            </div>
          </div>
        </a>

        <a
          href="http://localhost:9090"
          target="_blank"
          rel="noopener noreferrer"
          className="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div className="flex items-center gap-4">
            <div className="p-3 bg-red-100 rounded-lg">
              <Activity className="w-8 h-8 text-red-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">Prometheus</h4>
              <p className="text-sm text-gray-600">메트릭 수집 및 쿼리</p>
            </div>
          </div>
        </a>

        <a
          href="http://localhost:5601"
          target="_blank"
          rel="noopener noreferrer"
          className="card hover:shadow-lg transition-shadow cursor-pointer"
        >
          <div className="flex items-center gap-4">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Database className="w-8 h-8 text-purple-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900">Kibana</h4>
              <p className="text-sm text-gray-600">로그 분석 및 시각화</p>
            </div>
          </div>
        </a>
      </div>
    </div>
  )
}

export default Dashboard
