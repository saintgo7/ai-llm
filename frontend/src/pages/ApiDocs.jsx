import React, { useState } from 'react'
import { Code, Copy, Check, FileText, Zap, Shield } from 'lucide-react'
import toast from 'react-hot-toast'

function ApiDocs() {
  const [copiedIndex, setCopiedIndex] = useState(null)

  const copyToClipboard = (text, index) => {
    navigator.clipboard.writeText(text)
    setCopiedIndex(index)
    toast.success('클립보드에 복사되었습니다')
    setTimeout(() => setCopiedIndex(null), 2000)
  }

  const endpoints = [
    {
      method: 'GET',
      path: '/api/health',
      description: 'API 서버 상태 확인',
      example: `curl http://localhost:5000/api/health`,
      response: `{
  "status": "healthy",
  "timestamp": "2025-11-17T10:30:00Z"
}`,
    },
    {
      method: 'GET',
      path: '/api/tasks',
      description: '모든 작업 조회',
      example: `curl http://localhost:5000/api/tasks`,
      response: `[
  {
    "id": 1,
    "title": "프로젝트 기획서 작성",
    "description": "Q1 신규 프로젝트 기획서 초안 작성",
    "completed": false,
    "created_at": "2025-11-17T09:00:00Z"
  }
]`,
    },
    {
      method: 'POST',
      path: '/api/tasks',
      description: '새 작업 생성',
      example: `curl -X POST http://localhost:5000/api/tasks \\
  -H "Content-Type: application/json" \\
  -d '{"title":"새 작업","description":"작업 설명"}'`,
      response: `{
  "id": 2,
  "title": "새 작업",
  "description": "작업 설명",
  "completed": false,
  "created_at": "2025-11-17T10:30:00Z"
}`,
    },
    {
      method: 'GET',
      path: '/api/tasks/:id',
      description: '특정 작업 조회',
      example: `curl http://localhost:5000/api/tasks/1`,
      response: `{
  "id": 1,
  "title": "프로젝트 기획서 작성",
  "description": "Q1 신규 프로젝트 기획서 초안 작성",
  "completed": false,
  "created_at": "2025-11-17T09:00:00Z"
}`,
    },
    {
      method: 'PUT',
      path: '/api/tasks/:id',
      description: '작업 업데이트',
      example: `curl -X PUT http://localhost:5000/api/tasks/1 \\
  -H "Content-Type: application/json" \\
  -d '{"completed":true}'`,
      response: `{
  "id": 1,
  "title": "프로젝트 기획서 작성",
  "completed": true,
  "updated_at": "2025-11-17T10:30:00Z"
}`,
    },
    {
      method: 'DELETE',
      path: '/api/tasks/:id',
      description: '작업 삭제',
      example: `curl -X DELETE http://localhost:5000/api/tasks/1`,
      response: `{
  "message": "Task deleted successfully"
}`,
    },
    {
      method: 'POST',
      path: '/auth/api/login',
      description: '사용자 로그인',
      example: `curl -X POST http://localhost:5001/api/login \\
  -H "Content-Type: application/json" \\
  -d '{"username":"admin","password":"admin123"}'`,
      response: `{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "username": "admin",
    "role": "admin",
    "email": "admin@example.com"
  }
}`,
    },
    {
      method: 'GET',
      path: '/auth/api/verify',
      description: '토큰 검증',
      example: `curl http://localhost:5001/api/verify \\
  -H "Authorization: Bearer YOUR_TOKEN"`,
      response: `{
  "valid": true,
  "user": {
    "username": "admin",
    "role": "admin"
  }
}`,
    },
  ]

  const features = [
    {
      icon: Zap,
      title: 'RESTful API',
      description: 'REST 아키텍처 기반 표준 HTTP 메서드 지원',
    },
    {
      icon: Shield,
      title: 'JWT 인증',
      description: 'JSON Web Token 기반 보안 인증',
    },
    {
      icon: FileText,
      title: 'OpenAPI',
      description: 'OpenAPI 3.0 명세 완전 지원',
    },
    {
      icon: Code,
      title: 'Type Safety',
      description: '타입 검증 및 에러 핸들링',
    },
  ]

  const getMethodColor = (method) => {
    switch (method) {
      case 'GET':
        return 'bg-blue-100 text-blue-700 border-blue-300'
      case 'POST':
        return 'bg-green-100 text-green-700 border-green-300'
      case 'PUT':
        return 'bg-yellow-100 text-yellow-700 border-yellow-300'
      case 'DELETE':
        return 'bg-red-100 text-red-700 border-red-300'
      default:
        return 'bg-gray-100 text-gray-700 border-gray-300'
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">API 문서</h1>
        <p className="text-lg text-gray-600 mt-2">
          AI-LLM REST API 완전 가이드
        </p>
        <div className="flex justify-center gap-4 mt-4">
          <span className="badge badge-info">v2.0</span>
          <span className="badge badge-success">Production Ready</span>
        </div>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {features.map((feature, index) => {
          const Icon = feature.icon
          return (
            <div key={index} className="card text-center">
              <Icon className="w-12 h-12 text-primary-600 mx-auto mb-4" />
              <h3 className="font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-600">{feature.description}</p>
            </div>
          )
        })}
      </div>

      {/* Base URL */}
      <div className="card bg-gradient-to-r from-primary-50 to-primary-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">Base URL</h3>
        <div className="flex items-center gap-2">
          <code className="flex-1 bg-white px-4 py-3 rounded-lg text-gray-900 font-mono">
            http://localhost:5000
          </code>
          <button
            onClick={() =>
              copyToClipboard('http://localhost:5000', 'base-url')
            }
            className="btn btn-secondary"
          >
            {copiedIndex === 'base-url' ? (
              <Check className="w-5 h-5" />
            ) : (
              <Copy className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>

      {/* Endpoints */}
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-gray-900">엔드포인트</h2>

        {endpoints.map((endpoint, index) => (
          <div key={index} className="card">
            {/* Method and Path */}
            <div className="flex items-center gap-3 mb-4">
              <span
                className={`px-3 py-1 rounded-lg text-sm font-bold border-2 ${getMethodColor(
                  endpoint.method
                )}`}
              >
                {endpoint.method}
              </span>
              <code className="text-lg font-mono text-gray-900">
                {endpoint.path}
              </code>
            </div>

            {/* Description */}
            <p className="text-gray-700 mb-4">{endpoint.description}</p>

            {/* Example Request */}
            <div className="space-y-3">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-semibold text-gray-700">
                    요청 예제
                  </h4>
                  <button
                    onClick={() =>
                      copyToClipboard(endpoint.example, `example-${index}`)
                    }
                    className="text-gray-600 hover:text-primary-600 transition-colors"
                  >
                    {copiedIndex === `example-${index}` ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
                <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
                  <code>{endpoint.example}</code>
                </pre>
              </div>

              {/* Example Response */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h4 className="text-sm font-semibold text-gray-700">
                    응답 예제
                  </h4>
                  <button
                    onClick={() =>
                      copyToClipboard(endpoint.response, `response-${index}`)
                    }
                    className="text-gray-600 hover:text-primary-600 transition-colors"
                  >
                    {copiedIndex === `response-${index}` ? (
                      <Check className="w-4 h-4" />
                    ) : (
                      <Copy className="w-4 h-4" />
                    )}
                  </button>
                </div>
                <pre className="bg-gray-50 text-gray-900 p-4 rounded-lg overflow-x-auto border border-gray-200">
                  <code>{endpoint.response}</code>
                </pre>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Authentication */}
      <div className="card bg-yellow-50 border-2 border-yellow-200">
        <div className="flex items-start gap-3">
          <Shield className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              인증 방법
            </h3>
            <p className="text-gray-700 mb-4">
              보호된 엔드포인트에 접근하려면 JWT 토큰이 필요합니다:
            </p>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li>
                <code className="bg-white px-2 py-1 rounded">
                  /auth/api/login
                </code>
                으로 로그인하여 토큰 획득
              </li>
              <li>
                요청 헤더에{' '}
                <code className="bg-white px-2 py-1 rounded">
                  Authorization: Bearer YOUR_TOKEN
                </code>{' '}
                추가
              </li>
              <li>토큰은 1시간 동안 유효</li>
            </ol>
          </div>
        </div>
      </div>

      {/* Error Codes */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          HTTP 상태 코드
        </h3>
        <div className="space-y-2">
          <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <span className="badge badge-success">200</span>
            <span className="text-gray-700">성공 - 요청이 성공적으로 처리됨</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
            <span className="badge badge-success">201</span>
            <span className="text-gray-700">생성됨 - 리소스가 생성됨</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
            <span className="badge badge-info">204</span>
            <span className="text-gray-700">내용 없음 - 성공했으나 반환할 내용 없음</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <span className="badge badge-warning">400</span>
            <span className="text-gray-700">잘못된 요청 - 요청 형식이 올바르지 않음</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <span className="badge badge-warning">401</span>
            <span className="text-gray-700">인증 실패 - 유효한 토큰이 필요함</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
            <span className="badge badge-warning">404</span>
            <span className="text-gray-700">찾을 수 없음 - 리소스가 존재하지 않음</span>
          </div>
          <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
            <span className="badge badge-danger">500</span>
            <span className="text-gray-700">서버 오류 - 내부 서버 오류 발생</span>
          </div>
        </div>
      </div>

      {/* External Links */}
      <div className="card bg-primary-50 border-2 border-primary-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          추가 리소스
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <a
            href="http://localhost:5000/swagger"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-white rounded-lg hover:shadow-md transition-shadow"
          >
            <FileText className="w-8 h-8 text-primary-600" />
            <div>
              <h4 className="font-semibold text-gray-900">Swagger UI</h4>
              <p className="text-sm text-gray-600">
                인터랙티브 API 테스트
              </p>
            </div>
          </a>

          <a
            href="http://localhost:9090"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-white rounded-lg hover:shadow-md transition-shadow"
          >
            <Code className="w-8 h-8 text-primary-600" />
            <div>
              <h4 className="font-semibold text-gray-900">Prometheus</h4>
              <p className="text-sm text-gray-600">API 메트릭 및 모니터링</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  )
}

export default ApiDocs
