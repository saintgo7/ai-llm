# AI-LLM Frontend

React 기반 웹 프론트엔드 - 작업 관리, 실시간 채팅, 관리자 대시보드

## 🚀 기능

### 1. 작업 관리 (Task Manager)
- ✅ 작업 CRUD (생성, 조회, 수정, 삭제)
- 📊 작업 통계 (전체, 완료, 대기)
- 🔍 검색 및 필터링
- ✨ 실시간 업데이트
- 🎯 완료 상태 토글

### 2. 실시간 채팅 (WebSocket)
- 💬 실시간 메시지 전송
- 🏠 다중 대화방 지원 (일반, 개발, 지원)
- 👥 활성 사용자 수 표시
- 📱 모바일 반응형 디자인
- 🎨 사용자 구분 (본인/타인 메시지)

### 3. 관리자 대시보드
- 📈 실시간 시스템 메트릭
  - CPU 사용률
  - 메모리 사용률
  - 요청/초
  - 평균 응답시간
- 📊 차트 시각화 (Recharts)
  - 요청 및 오류율 (Area Chart)
  - 응답시간 (Line Chart)
  - 시스템 리소스 (Bar Chart)
- 🔧 서비스 상태 모니터링
- 🚨 알림 및 경고
- 🔗 외부 도구 연동 (Grafana, Prometheus, Kibana)

### 4. API 문서
- 📖 전체 엔드포인트 문서화
- 💻 요청/응답 예제
- 📋 클립보드 복사 기능
- 🔐 인증 방법 안내
- ⚡ HTTP 상태 코드 설명

## 🛠️ 기술 스택

### Core
- **React 18.2** - UI 라이브러리
- **Vite 5.0** - 빌드 도구
- **React Router 6** - 클라이언트 라우팅

### State Management & Data Fetching
- **Zustand** - 전역 상태 관리
- **React Query** - 서버 상태 관리 및 캐싱
- **Axios** - HTTP 클라이언트

### UI & Styling
- **Tailwind CSS** - 유틸리티 기반 CSS
- **Lucide React** - 아이콘 라이브러리
- **React Hot Toast** - 알림 시스템

### Charts & Visualization
- **Recharts** - 차트 라이브러리

### Real-time Communication
- **Socket.io Client** - WebSocket 클라이언트

### Utilities
- **date-fns** - 날짜 포맷팅
- **clsx** - 클래스명 관리

## 📦 설치 및 실행

### 개발 환경

```bash
# 의존성 설치
npm install

# 개발 서버 시작 (포트 3001)
npm run dev

# 브라우저 자동 열기
open http://localhost:3001
```

### 프로덕션 빌드

```bash
# 프로덕션 빌드
npm run build

# 빌드 결과 미리보기
npm run preview
```

### Docker

```bash
# Docker 이미지 빌드
docker build -t ai-llm-frontend .

# 컨테이너 실행
docker run -p 8080:80 ai-llm-frontend

# 접속
open http://localhost:8080
```

## 📁 프로젝트 구조

```
frontend/
├── public/                 # 정적 파일
├── src/
│   ├── components/        # 재사용 가능한 컴포넌트
│   │   └── Layout.jsx    # 레이아웃 (헤더, 네비게이션, 푸터)
│   ├── pages/            # 페이지 컴포넌트
│   │   ├── Login.jsx     # 로그인 페이지
│   │   ├── TaskManager.jsx  # 작업 관리
│   │   ├── Chat.jsx      # 실시간 채팅
│   │   ├── Dashboard.jsx # 관리자 대시보드
│   │   └── ApiDocs.jsx   # API 문서
│   ├── store/            # 전역 상태
│   │   └── authStore.js  # 인증 상태 (Zustand)
│   ├── lib/              # 유틸리티
│   │   └── api.js        # API 클라이언트
│   ├── index.css         # 글로벌 스타일
│   ├── App.jsx           # 메인 앱 컴포넌트
│   └── main.jsx          # 진입점
├── Dockerfile            # Docker 설정
├── nginx.conf            # Nginx 설정
├── vite.config.js        # Vite 설정
├── tailwind.config.js    # Tailwind 설정
└── package.json          # 의존성 및 스크립트
```

## 🔧 환경 설정

### Vite 프록시 설정

개발 환경에서 API 요청을 프록시합니다:

```javascript
// vite.config.js
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:5000',
      '/auth': 'http://localhost:5001',
      '/socket.io': {
        target: 'http://localhost:5002',
        ws: true,
      },
    },
  },
})
```

### Nginx 프록시 설정

프로덕션 환경에서 API 요청을 프록시합니다:

```nginx
# nginx.conf
location /api/ {
  proxy_pass http://api-server:5000/api/;
}
```

## 🎨 컴포넌트 가이드

### Layout 컴포넌트

모든 페이지의 공통 레이아웃:
- 헤더 (로고, 네비게이션, 사용자 메뉴)
- 메인 콘텐츠 영역
- 푸터

### 페이지 컴포넌트

#### TaskManager
- 작업 목록 표시
- 작업 생성/수정 모달
- 검색 및 필터링
- 통계 카드

#### Chat
- WebSocket 연결 관리
- 메시지 송수신
- 대화방 전환
- 사용자 목록

#### Dashboard
- 실시간 메트릭 표시
- 차트 렌더링
- 서비스 상태 모니터링
- 알림 표시

#### ApiDocs
- 엔드포인트 문서
- 코드 예제
- 클립보드 복사
- HTTP 상태 코드 설명

## 🔐 인증

### 로그인 플로우

1. 사용자가 로그인 페이지에서 인증 정보 입력
2. `/auth/api/login`에 POST 요청
3. JWT 토큰 수신 및 Zustand 스토어에 저장
4. 로컬 스토리지에 영구 저장 (persist 미들웨어)
5. API 요청 시 `Authorization` 헤더에 토큰 자동 포함

### 보호된 라우트

```jsx
<Route
  path="/tasks"
  element={isAuthenticated ? <TaskManager /> : <Navigate to="/login" />}
/>
```

### API 인터셉터

```javascript
// 요청 인터셉터 - 토큰 추가
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 응답 인터셉터 - 401 처리
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

## 📊 상태 관리

### Zustand (전역 상태)

```javascript
// authStore.js
export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
    }),
    { name: 'auth-storage' }
  )
)
```

### React Query (서버 상태)

```javascript
// 데이터 페칭
const { data, isLoading } = useQuery('tasks', taskApi.getAll)

// 뮤테이션
const createMutation = useMutation(taskApi.create, {
  onSuccess: () => {
    queryClient.invalidateQueries('tasks')
  },
})
```

## 🎯 주요 기능 구현

### 실시간 채팅 (WebSocket)

```javascript
// Socket.io 연결
const socket = io('http://localhost:5002')

// 이벤트 리스너
socket.on('new_message', (data) => {
  setMessages((prev) => [...prev, data])
})

// 메시지 전송
socket.emit('message', { username, message, room })
```

### 차트 시각화

```javascript
// Recharts 사용
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={chartData}>
    <CartesianGrid strokeDasharray="3 3" />
    <XAxis dataKey="time" />
    <YAxis />
    <Tooltip />
    <Line type="monotone" dataKey="latency" stroke="#8b5cf6" />
  </LineChart>
</ResponsiveContainer>
```

## 🚀 배포

### Docker Compose

```yaml
# docker-compose.yml
frontend:
  build: ./frontend
  ports:
    - "8080:80"
  depends_on:
    - api-server
    - auth-server
```

### Nginx 프로덕션 설정

- Gzip 압축
- 정적 파일 캐싱 (1년)
- 보안 헤더
- API 프록시
- React Router 지원 (SPA)

## 🧪 테스트

```bash
# 린팅
npm run lint

# 타입 체크 (TypeScript 사용 시)
npm run type-check
```

## 📱 반응형 디자인

Tailwind CSS 브레이크포인트:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

모바일, 태블릿, 데스크톱 모두 지원합니다.

## 🎨 커스터마이징

### 색상 변경

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#0ea5e9', // 기본 색상 변경
        },
      },
    },
  },
}
```

### 컴포넌트 스타일

```css
/* index.css */
.btn-primary {
  @apply bg-primary-600 text-white hover:bg-primary-700;
}
```

## 🐛 문제 해결

### CORS 오류
- Vite 프록시 설정 확인
- 백엔드 CORS 설정 확인

### WebSocket 연결 실패
- WebSocket 서버 실행 확인
- 포트 5002 사용 가능 확인

### 빌드 오류
- Node.js 버전 확인 (18+)
- `node_modules` 삭제 후 재설치

## 📚 참고 자료

- [React 공식 문서](https://react.dev/)
- [Vite 문서](https://vitejs.dev/)
- [Tailwind CSS 문서](https://tailwindcss.com/)
- [React Query 문서](https://tanstack.com/query/latest)
- [Zustand 문서](https://github.com/pmndrs/zustand)
- [Socket.io 클라이언트 문서](https://socket.io/docs/v4/client-api/)

## 📝 라이선스

MIT License

---

**마지막 업데이트:** 2025-11-17
**버전:** 1.0.0
