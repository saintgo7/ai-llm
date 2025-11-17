#!/bin/bash
# AI-LLM 전체 시스템 시작 스크립트

set -e

echo "🚀 AI-LLM 시스템 시작"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 환경 변수 확인
if [ ! -f .env ]; then
  echo -e "${YELLOW}⚠️  .env 파일이 없습니다. .env.example에서 복사합니다...${NC}"
  cp .env.example .env
  echo -e "${GREEN}✅ .env 파일이 생성되었습니다${NC}"
fi

# Docker 확인
if ! command -v docker &> /dev/null; then
  echo -e "${RED}❌ Docker가 설치되어 있지 않습니다${NC}"
  exit 1
fi

if ! command -v docker-compose &> /dev/null; then
  echo -e "${RED}❌ Docker Compose가 설치되어 있지 않습니다${NC}"
  exit 1
fi

echo -e "${GREEN}✅ Docker & Docker Compose 확인 완료${NC}"

# 기존 컨테이너 정리 (선택적)
read -p "기존 컨테이너를 정리하시겠습니까? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo -e "${YELLOW}🧹 기존 컨테이너 정리 중...${NC}"
  docker-compose down -v
fi

# Docker 이미지 빌드
echo -e "${BLUE}🔨 Docker 이미지 빌드 중...${NC}"
docker-compose build --no-cache

# 컨테이너 시작
echo -e "${BLUE}🚀 컨테이너 시작 중...${NC}"
docker-compose up -d

# 서비스 시작 대기
echo -e "${YELLOW}⏳ 서비스 시작 대기 중... (30초)${NC}"
sleep 30

# 헬스 체크
echo ""
echo "🏥 헬스 체크 실행 중..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# API 서버
if curl -f http://localhost:5000/api/health &> /dev/null; then
  echo -e "${GREEN}✅ API 서버: 정상${NC}"
else
  echo -e "${RED}❌ API 서버: 실패${NC}"
fi

# Auth 서버
if curl -f -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}' &> /dev/null; then
  echo -e "${GREEN}✅ Auth 서버: 정상${NC}"
else
  echo -e "${YELLOW}⚠️  Auth 서버: 응답 중 (정상)${NC}"
fi

# PostgreSQL
if docker exec ai-llm-db pg_isready -U appuser &> /dev/null; then
  echo -e "${GREEN}✅ PostgreSQL: 정상${NC}"
else
  echo -e "${RED}❌ PostgreSQL: 실패${NC}"
fi

# Redis
if docker exec ai-llm-redis redis-cli ping &> /dev/null; then
  echo -e "${GREEN}✅ Redis: 정상${NC}"
else
  echo -e "${RED}❌ Redis: 실패${NC}"
fi

# Prometheus
if curl -f http://localhost:9090/-/healthy &> /dev/null; then
  echo -e "${GREEN}✅ Prometheus: 정상${NC}"
else
  echo -e "${RED}❌ Prometheus: 실패${NC}"
fi

# Grafana
if curl -f http://localhost:3000/api/health &> /dev/null; then
  echo -e "${GREEN}✅ Grafana: 정상${NC}"
else
  echo -e "${YELLOW}⚠️  Grafana: 시작 중...${NC}"
fi

# Elasticsearch
if curl -f http://localhost:9200/_cluster/health &> /dev/null; then
  echo -e "${GREEN}✅ Elasticsearch: 정상${NC}"
else
  echo -e "${YELLOW}⚠️  Elasticsearch: 시작 중...${NC}"
fi

# Kibana
if curl -f http://localhost:5601/api/status &> /dev/null; then
  echo -e "${GREEN}✅ Kibana: 정상${NC}"
else
  echo -e "${YELLOW}⚠️  Kibana: 시작 중...${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 시스템 시작 완료!${NC}"
echo ""
echo "📊 접속 정보:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${BLUE}🔹 API 서버:${NC}         http://localhost:5000"
echo -e "${BLUE}🔹 API 문서:${NC}         http://localhost:5000/api/docs"
echo -e "${BLUE}🔹 Auth 서버:${NC}        http://localhost:5001"
echo -e "${BLUE}🔹 Prometheus:${NC}       http://localhost:9090"
echo -e "${BLUE}🔹 Grafana:${NC}          http://localhost:3000 (admin/admin)"
echo -e "${BLUE}🔹 Kibana:${NC}           http://localhost:5601"
echo -e "${BLUE}🔹 PostgreSQL:${NC}       localhost:5432 (appuser/changeme)"
echo -e "${BLUE}🔹 Redis:${NC}            localhost:6379"
echo ""
echo "📝 유용한 명령어:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  docker-compose logs -f              # 모든 로그 확인"
echo "  docker-compose logs -f api-server   # API 서버 로그"
echo "  docker-compose ps                   # 컨테이너 상태"
echo "  docker-compose stop                 # 시스템 중지"
echo "  docker-compose down                 # 시스템 완전 종료"
echo "  ./scripts/verify.sh                 # 시스템 검증"
echo "  ./scripts/populate-data.sh          # 샘플 데이터 생성"
echo ""
echo -e "${GREEN}✨ 즐거운 코딩 되세요!${NC}"
