#!/bin/bash
# AI-LLM 샘플 데이터 생성 스크립트

set -e

echo "📊 AI-LLM 샘플 데이터 생성 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
API_URL="http://localhost:5000"
AUTH_URL="http://localhost:5001"
CREATED_COUNT=0
FAILED_COUNT=0

# Wait for services to be ready
echo ""
echo "⏳ 서비스 준비 대기 중..."
for i in {1..30}; do
  if curl -sf $API_URL/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API 서버 준비 완료${NC}"
    break
  fi
  if [ $i -eq 30 ]; then
    echo -e "${RED}❌ API 서버가 준비되지 않았습니다${NC}"
    exit 1
  fi
  sleep 2
done

echo ""
echo "👤 사용자 인증 및 토큰 획득"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Login and get token
TOKEN=$(curl -s -X POST $AUTH_URL/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))" 2>/dev/null)

if [ -n "$TOKEN" ]; then
  echo -e "${GREEN}✅ 로그인 성공 (Token: ${TOKEN:0:20}...)${NC}"
else
  echo -e "${YELLOW}⚠️  인증 토큰을 얻지 못했습니다. 계속 진행합니다...${NC}"
fi

echo ""
echo "📝 작업(Tasks) 샘플 데이터 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Sample tasks data
declare -a TASKS=(
  '{"title":"프로젝트 기획서 작성","description":"Q1 신규 프로젝트 기획서 초안 작성 및 검토"}'
  '{"title":"API 문서 업데이트","description":"REST API v2.0 문서 업데이트 및 Swagger 설정"}'
  '{"title":"데이터베이스 마이그레이션","description":"PostgreSQL 14.7로 버전 업그레이드 및 스키마 마이그레이션"}'
  '{"title":"보안 취약점 점검","description":"OWASP Top 10 기준 보안 취약점 스캔 및 패치"}'
  '{"title":"CI/CD 파이프라인 구축","description":"GitHub Actions 기반 자동 배포 파이프라인 설정"}'
  '{"title":"모니터링 시스템 구축","description":"Prometheus + Grafana 대시보드 설정 완료"}'
  '{"title":"성능 테스트 실행","description":"Locust를 이용한 부하 테스트 및 병목 지점 분석"}'
  '{"title":"코드 리뷰","description":"main 브랜치 병합 전 코드 리뷰 및 피드백 반영"}'
  '{"title":"유닛 테스트 작성","description":"핵심 비즈니스 로직 테스트 커버리지 80% 달성"}'
  '{"title":"배포 준비","description":"프로덕션 환경 배포 체크리스트 검토 및 롤백 계획 수립"}'
  '{"title":"사용자 피드백 분석","description":"지난 주 사용자 피드백 100건 분석 및 개선사항 도출"}'
  '{"title":"기술 문서 작성","description":"새로운 아키텍처 패턴 적용 사례 문서화"}'
  '{"title":"장애 대응 훈련","description":"장애 시나리오별 대응 매뉴얼 작성 및 모의 훈련"}'
  '{"title":"리팩토링","description":"레거시 코드 리팩토링 및 기술 부채 해소"}'
  '{"title":"신규 기능 개발","description":"실시간 알림 기능 WebSocket 기반 구현"}'
)

for task_data in "${TASKS[@]}"; do
  response=$(curl -s -w "\n%{http_code}" -X POST $API_URL/api/tasks \
    -H "Content-Type: application/json" \
    -d "$task_data")

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | sed '$d')

  if [ "$http_code" == "201" ]; then
    task_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', 'N/A'))" 2>/dev/null)
    title=$(echo "$task_data" | python3 -c "import sys, json; print(json.loads(sys.stdin.read()).get('title', 'N/A'))")
    echo -e "${GREEN}✅ 작업 생성됨 (ID: $task_id) - $title${NC}"
    ((CREATED_COUNT++))
  else
    echo -e "${RED}❌ 작업 생성 실패 (HTTP $http_code)${NC}"
    ((FAILED_COUNT++))
  fi
  sleep 0.2
done

echo ""
echo "🔄 일부 작업 완료 처리"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get all tasks and mark some as completed
ALL_TASKS=$(curl -s $API_URL/api/tasks)
TASK_IDS=$(echo "$ALL_TASKS" | python3 -c "import sys, json; tasks = json.load(sys.stdin); print(' '.join([str(t['id']) for t in tasks[:5]]))" 2>/dev/null)

if [ -n "$TASK_IDS" ]; then
  for task_id in $TASK_IDS; do
    response=$(curl -s -w "\n%{http_code}" -X PUT $API_URL/api/tasks/$task_id \
      -H "Content-Type: application/json" \
      -d '{"completed":true}')

    http_code=$(echo "$response" | tail -n1)

    if [ "$http_code" == "200" ]; then
      echo -e "${GREEN}✅ 작업 완료 처리 (ID: $task_id)${NC}"
    else
      echo -e "${YELLOW}⚠️  작업 완료 처리 실패 (ID: $task_id, HTTP $http_code)${NC}"
    fi
    sleep 0.1
  done
else
  echo -e "${YELLOW}⚠️  작업 목록을 가져올 수 없습니다${NC}"
fi

echo ""
echo "💾 Redis 캐시 데이터 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Sample Redis data
declare -a REDIS_KEYS=(
  "user:1001:name John Doe"
  "user:1002:name Jane Smith"
  "user:1003:name Bob Johnson"
  "session:sess_abc123 active"
  "session:sess_def456 active"
  "cache:api:tasks pending"
  "counter:api_requests 1234"
  "counter:active_users 42"
  "config:feature:dark_mode enabled"
  "config:feature:notifications enabled"
)

for redis_cmd in "${REDIS_KEYS[@]}"; do
  key=$(echo $redis_cmd | awk '{print $1}')
  value="${redis_cmd#* }"

  result=$(docker exec ai-llm-redis redis-cli SET "$key" "$value" 2>/dev/null)

  if [ "$result" == "OK" ]; then
    echo -e "${GREEN}✅ Redis 키 설정: $key${NC}"
  else
    echo -e "${RED}❌ Redis 키 설정 실패: $key${NC}"
  fi
  sleep 0.1
done

# Set expiration on session keys
docker exec ai-llm-redis redis-cli EXPIRE "session:sess_abc123" 3600 > /dev/null 2>&1
docker exec ai-llm-redis redis-cli EXPIRE "session:sess_def456" 3600 > /dev/null 2>&1
echo -e "${BLUE}🕐 세션 키에 TTL 설정 (1시간)${NC}"

echo ""
echo "🗄️  PostgreSQL 샘플 데이터 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create sample tables and data in PostgreSQL
docker exec ai-llm-db psql -U appuser -d appdb << 'EOF' 2>/dev/null

-- 사용자 테이블
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 사용자 데이터
INSERT INTO users (username, email, role) VALUES
    ('admin', 'admin@example.com', 'admin'),
    ('john_doe', 'john@example.com', 'user'),
    ('jane_smith', 'jane@example.com', 'user'),
    ('bob_johnson', 'bob@example.com', 'moderator'),
    ('alice_williams', 'alice@example.com', 'user')
ON CONFLICT (username) DO NOTHING;

-- 태스크 통계 테이블
CREATE TABLE IF NOT EXISTS task_stats (
    id SERIAL PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    pending_tasks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 오늘의 통계
INSERT INTO task_stats (total_tasks, completed_tasks, pending_tasks)
VALUES (15, 5, 10);

-- API 요청 로그 테이블
CREATE TABLE IF NOT EXISTS api_logs (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(200),
    method VARCHAR(10),
    status_code INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 로그 데이터
INSERT INTO api_logs (endpoint, method, status_code, response_time_ms) VALUES
    ('/api/tasks', 'GET', 200, 45),
    ('/api/tasks', 'POST', 201, 78),
    ('/api/tasks/1', 'PUT', 200, 52),
    ('/api/tasks/2', 'DELETE', 204, 38),
    ('/api/health', 'GET', 200, 12);

EOF

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✅ PostgreSQL 테이블 및 샘플 데이터 생성 완료${NC}"

  # Show user count
  USER_COUNT=$(docker exec ai-llm-db psql -U appuser -d appdb -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | xargs)
  echo -e "${BLUE}📊 사용자 수: $USER_COUNT${NC}"

  # Show task stats
  STATS=$(docker exec ai-llm-db psql -U appuser -d appdb -t -c "SELECT total_tasks, completed_tasks, pending_tasks FROM task_stats ORDER BY id DESC LIMIT 1;" 2>/dev/null)
  echo -e "${BLUE}📊 작업 통계: $STATS${NC}"
else
  echo -e "${RED}❌ PostgreSQL 데이터 생성 실패${NC}"
fi

echo ""
echo "📈 메트릭 데이터 생성"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Generate some API traffic for metrics
echo -n "API 트래픽 생성 중"
for i in {1..20}; do
  curl -s $API_URL/api/health > /dev/null 2>&1 &
  curl -s $API_URL/api/tasks > /dev/null 2>&1 &
  echo -n "."
  sleep 0.5
done
wait
echo ""
echo -e "${GREEN}✅ 메트릭 데이터 생성 완료 (20개 요청)${NC}"

echo ""
echo "🔍 데이터 검증"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verify API tasks
TASK_COUNT=$(curl -s $API_URL/api/tasks | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
if [ -n "$TASK_COUNT" ]; then
  echo -e "${GREEN}✅ API 작업 수: $TASK_COUNT개${NC}"
else
  echo -e "${YELLOW}⚠️  API 작업 수를 확인할 수 없습니다${NC}"
fi

# Verify Redis keys
REDIS_KEY_COUNT=$(docker exec ai-llm-redis redis-cli DBSIZE 2>/dev/null | grep -oP '\d+')
if [ -n "$REDIS_KEY_COUNT" ]; then
  echo -e "${GREEN}✅ Redis 키 수: $REDIS_KEY_COUNT개${NC}"
else
  echo -e "${YELLOW}⚠️  Redis 키 수를 확인할 수 없습니다${NC}"
fi

# Verify PostgreSQL users
PG_USER_COUNT=$(docker exec ai-llm-db psql -U appuser -d appdb -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | xargs)
if [ -n "$PG_USER_COUNT" ]; then
  echo -e "${GREEN}✅ PostgreSQL 사용자 수: $PG_USER_COUNT명${NC}"
else
  echo -e "${YELLOW}⚠️  PostgreSQL 데이터를 확인할 수 없습니다${NC}"
fi

# Verify Prometheus metrics
PROM_TARGETS=$(curl -s http://localhost:9090/api/v1/targets 2>/dev/null | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('data', {}).get('activeTargets', [])))" 2>/dev/null)
if [ -n "$PROM_TARGETS" ] && [ "$PROM_TARGETS" -gt 0 ]; then
  echo -e "${GREEN}✅ Prometheus 활성 타겟: $PROM_TARGETS개${NC}"
else
  echo -e "${YELLOW}⚠️  Prometheus 타겟을 확인할 수 없습니다${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "결과 요약"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}생성 성공: $CREATED_COUNT개${NC}"
echo -e "${RED}생성 실패: $FAILED_COUNT개${NC}"
echo ""
echo "📊 생성된 데이터:"
echo "  - REST API 작업: $TASK_COUNT개"
echo "  - Redis 캐시 키: $REDIS_KEY_COUNT개"
echo "  - PostgreSQL 사용자: $PG_USER_COUNT명"
echo "  - Prometheus 타겟: $PROM_TARGETS개"
echo ""
echo "🌐 접속 정보:"
echo "  - API Server: http://localhost:5000/api/tasks"
echo "  - Auth Server: http://localhost:5001/api/login"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo "  - Kibana: http://localhost:5601"
echo ""
echo -e "${GREEN}🎉 샘플 데이터 생성 완료!${NC}"
echo ""
echo "다음 단계:"
echo "  1. 웹 브라우저에서 Grafana 대시보드 확인"
echo "  2. API 엔드포인트 테스트: curl http://localhost:5000/api/tasks"
echo "  3. 시스템 검증: ./scripts/verify.sh"
