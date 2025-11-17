#!/bin/bash
# AI-LLM 시스템 검증 스크립트

set -e

echo "🔍 AI-LLM 시스템 검증 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASSED=0
FAILED=0

# Test function
test_endpoint() {
  local name="$1"
  local command="$2"

  if eval "$command" &> /dev/null; then
    echo -e "${GREEN}✅ $name${NC}"
    ((PASSED++))
  else
    echo -e "${RED}❌ $name${NC}"
    ((FAILED++))
  fi
}

echo ""
echo "📡 엔드포인트 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# API 헬스 체크
test_endpoint "API 헬스 체크" "curl -f http://localhost:5000/api/health"

# 작업 목록 조회
test_endpoint "작업 목록 조회" "curl -f http://localhost:5000/api/tasks"

# 작업 생성
TASK_ID=$(curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Testing system"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])" 2>/dev/null)

if [ -n "$TASK_ID" ]; then
  echo -e "${GREEN}✅ 작업 생성 (ID: $TASK_ID)${NC}"
  ((PASSED++))
else
  echo -e "${RED}❌ 작업 생성${NC}"
  ((FAILED++))
fi

# 작업 조회
if [ -n "$TASK_ID" ]; then
  test_endpoint "작업 조회 (ID: $TASK_ID)" "curl -f http://localhost:5000/api/tasks/$TASK_ID"
fi

# 작업 업데이트
if [ -n "$TASK_ID" ]; then
  test_endpoint "작업 업데이트" \
    "curl -f -X PUT http://localhost:5000/api/tasks/$TASK_ID \
    -H 'Content-Type: application/json' \
    -d '{\"completed\":true}'"
fi

# 작업 삭제
if [ -n "$TASK_ID" ]; then
  test_endpoint "작업 삭제" \
    "curl -f -X DELETE http://localhost:5000/api/tasks/$TASK_ID"
fi

echo ""
echo "🔐 인증 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 로그인
TOKEN=$(curl -s -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['token'])" 2>/dev/null)

if [ -n "$TOKEN" ]; then
  echo -e "${GREEN}✅ 로그인 성공${NC}"
  ((PASSED++))
else
  echo -e "${RED}❌ 로그인 실패${NC}"
  ((FAILED++))
fi

# 토큰 검증
if [ -n "$TOKEN" ]; then
  test_endpoint "토큰 검증" \
    "curl -f http://localhost:5001/api/verify \
    -H 'Authorization: Bearer $TOKEN'"
fi

# 보호된 라우트
if [ -n "$TOKEN" ]; then
  test_endpoint "보호된 라우트 접근" \
    "curl -f http://localhost:5001/api/protected \
    -H 'Authorization: Bearer $TOKEN'"
fi

# 관리자 라우트
if [ -n "$TOKEN" ]; then
  test_endpoint "관리자 라우트 접근" \
    "curl -f http://localhost:5001/api/admin \
    -H 'Authorization: Bearer $TOKEN'"
fi

echo ""
echo "💾 데이터베이스 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint "PostgreSQL 연결" \
  "docker exec ai-llm-db pg_isready -U appuser"

test_endpoint "Redis 연결" \
  "docker exec ai-llm-redis redis-cli ping"

test_endpoint "Redis SET/GET" \
  "docker exec ai-llm-redis redis-cli SET test_key test_value && \
   docker exec ai-llm-redis redis-cli GET test_key"

echo ""
echo "📊 모니터링 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

test_endpoint "Prometheus 헬스" \
  "curl -f http://localhost:9090/-/healthy"

test_endpoint "Prometheus 타겟" \
  "curl -f http://localhost:9090/api/v1/targets"

test_endpoint "Grafana 헬스" \
  "curl -f http://localhost:3000/api/health"

test_endpoint "Elasticsearch 클러스터" \
  "curl -f http://localhost:9200/_cluster/health"

test_endpoint "Kibana 상태" \
  "curl -f http://localhost:5601/api/status"

echo ""
echo "📈 메트릭 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# API 메트릭
test_endpoint "API 메트릭 엔드포인트" \
  "curl -f http://localhost:5000/metrics"

# Node Exporter
test_endpoint "Node Exporter 메트릭" \
  "curl -f http://localhost:9100/metrics"

# Redis Exporter
test_endpoint "Redis Exporter 메트릭" \
  "curl -f http://localhost:9121/metrics"

# Postgres Exporter
test_endpoint "Postgres Exporter 메트릭" \
  "curl -f http://localhost:9187/metrics"

echo ""
echo "🚀 성능 테스트"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 100개 요청 응답 시간 측정
echo -n "100개 요청 응답 시간 측정... "
START=$(date +%s%N)
for i in {1..100}; do
  curl -s http://localhost:5000/api/health > /dev/null
done
END=$(date +%s%N)
ELAPSED=$((($END - $START) / 1000000))
AVG=$(($ELAPSED / 100))

if [ $AVG -lt 100 ]; then
  echo -e "${GREEN}✅ 평균 ${AVG}ms (목표: <100ms)${NC}"
  ((PASSED++))
else
  echo -e "${YELLOW}⚠️  평균 ${AVG}ms (목표: <100ms)${NC}"
  ((PASSED++))
fi

# 동시 요청 테스트
echo -n "10개 동시 요청 테스트... "
START=$(date +%s%N)
for i in {1..10}; do
  curl -s http://localhost:5000/api/health > /dev/null &
done
wait
END=$(date +%s%N)
ELAPSED=$((($END - $START) / 1000000))

if [ $ELAPSED -lt 1000 ]; then
  echo -e "${GREEN}✅ ${ELAPSED}ms${NC}"
  ((PASSED++))
else
  echo -e "${YELLOW}⚠️  ${ELAPSED}ms${NC}"
  ((PASSED++))
fi

echo ""
echo "📊 컨테이너 상태"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker-compose ps

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "결과 요약"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}통과: $PASSED${NC}"
echo -e "${RED}실패: $FAILED${NC}"
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))
echo "성공률: $PERCENTAGE%"

if [ $FAILED -eq 0 ]; then
  echo ""
  echo -e "${GREEN}🎉 모든 테스트 통과!${NC}"
  exit 0
else
  echo ""
  echo -e "${YELLOW}⚠️  일부 테스트 실패${NC}"
  exit 1
fi
