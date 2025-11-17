# AI-LLM Scripts

실전 실행 및 검증을 위한 자동화 스크립트 모음입니다.

## 📁 스크립트 목록

### 1. start.sh - 시스템 시작 스크립트

전체 AI-LLM 시스템을 시작하고 헬스 체크를 수행합니다.

**기능:**
- 환경 검증 (Docker, Docker Compose)
- 기존 컨테이너 정리 옵션
- Docker 이미지 빌드
- 13개 서비스 시작 (API, Auth, DB, Redis, Monitoring Stack)
- 각 서비스별 헬스 체크
- 접속 정보 표시

**사용법:**
```bash
./scripts/start.sh
```

**시작되는 서비스:**
- ✅ API Server (포트 5000)
- ✅ Auth Server (포트 5001)
- ✅ PostgreSQL (포트 5432)
- ✅ Redis (포트 6379)
- ✅ Prometheus (포트 9090)
- ✅ Grafana (포트 3000)
- ✅ Elasticsearch (포트 9200)
- ✅ Kibana (포트 5601)
- ✅ Logstash (포트 5044)
- ✅ Node Exporter (포트 9100)
- ✅ Redis Exporter (포트 9121)
- ✅ Postgres Exporter (포트 9187)

---

### 2. populate-data.sh - 샘플 데이터 생성 스크립트

테스트 및 데모를 위한 샘플 데이터를 생성합니다.

**기능:**
- 15개 샘플 작업(Task) 생성
- 일부 작업 완료 처리
- Redis 캐시 데이터 생성 (10개 키)
- PostgreSQL 테이블 및 샘플 데이터 생성
  - users 테이블 (5명의 사용자)
  - task_stats 테이블 (통계 데이터)
  - api_logs 테이블 (로그 데이터)
- 메트릭 데이터 생성 (20개 API 요청)
- 데이터 검증 및 요약

**사용법:**
```bash
# 시스템이 실행 중이어야 합니다
./scripts/populate-data.sh
```

**생성되는 데이터:**
- 📝 REST API 작업: 15개
- 💾 Redis 캐시 키: 10개
- 👥 PostgreSQL 사용자: 5명
- 📊 작업 통계 및 로그 데이터
- 📈 Prometheus 메트릭 데이터

---

### 3. verify.sh - 시스템 검증 스크립트

전체 시스템의 기능을 자동으로 테스트하고 검증합니다.

**기능:**
- **API 엔드포인트 테스트** (7개)
  - Health check
  - Task CRUD 작업 (생성, 조회, 목록, 업데이트, 삭제)
- **인증 테스트** (4개)
  - 로그인
  - 토큰 검증
  - 보호된 라우트 접근
  - 관리자 라우트 접근
- **데이터베이스 테스트** (3개)
  - PostgreSQL 연결
  - Redis 연결 및 SET/GET
- **모니터링 테스트** (5개)
  - Prometheus 헬스 및 타겟
  - Grafana 헬스
  - Elasticsearch 클러스터
  - Kibana 상태
- **메트릭 테스트** (4개)
  - API 메트릭
  - Node Exporter
  - Redis Exporter
  - Postgres Exporter
- **성능 테스트** (2개)
  - 100개 요청 응답 시간 측정
  - 10개 동시 요청 테스트
- 결과 요약 및 성공률 표시

**사용법:**
```bash
# 시스템이 실행 중이어야 합니다
./scripts/verify.sh
```

**테스트 결과:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
결과 요약
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
통과: 25
실패: 0
성공률: 100%

🎉 모든 테스트 통과!
```

---

## 🚀 빠른 시작 가이드

### 전체 시스템 실행 3단계

#### 1단계: 시스템 시작
```bash
./scripts/start.sh
```
- 모든 서비스가 시작될 때까지 대기 (약 1-2분)
- 헬스 체크 통과 확인

#### 2단계: 샘플 데이터 생성
```bash
./scripts/populate-data.sh
```
- 테스트용 샘플 데이터 생성 (약 30초)
- 생성된 데이터 개수 확인

#### 3단계: 시스템 검증
```bash
./scripts/verify.sh
```
- 전체 시스템 자동 검증 (약 2분)
- 모든 테스트 통과 확인

---

## 📊 시스템 모니터링

### Grafana 대시보드
```bash
# 브라우저에서 접속
http://localhost:3000

# 기본 로그인
Username: admin
Password: admin
```

**대시보드 패널:**
- Request Rate (초당 요청 수)
- Response Time (p95, p99)
- Error Rate (5xx 에러 비율)
- Active Connections
- CPU Usage
- Memory Usage
- Database Connections

### Prometheus 메트릭
```bash
# Prometheus UI 접속
http://localhost:9090

# 메트릭 확인
http://localhost:5000/metrics        # API 메트릭
http://localhost:9100/metrics        # Node Exporter
http://localhost:9121/metrics        # Redis Exporter
http://localhost:9187/metrics        # Postgres Exporter
```

### Kibana 로그 분석
```bash
# Kibana 접속
http://localhost:5601

# Index Pattern 생성
logstash-*
```

---

## 🛠️ 유용한 명령어

### 컨테이너 상태 확인
```bash
docker-compose ps
```

### 로그 확인
```bash
# 전체 로그
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f api-server
docker-compose logs -f auth-server

# 최근 100줄
docker-compose logs --tail=100 api-server
```

### 데이터베이스 접속
```bash
# PostgreSQL
docker exec -it ai-llm-db psql -U appuser -d appdb

# Redis
docker exec -it ai-llm-redis redis-cli
```

### API 테스트
```bash
# Health Check
curl http://localhost:5000/api/health

# 작업 목록 조회
curl http://localhost:5000/api/tasks

# 작업 생성
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Testing"}'

# 로그인
curl -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 시스템 정리
```bash
# 컨테이너 중지
docker-compose down

# 컨테이너 + 볼륨 삭제
docker-compose down -v

# 이미지까지 삭제
docker-compose down -v --rmi all
```

---

## 🐛 트러블슈팅

### 포트 충돌
**증상:** 포트가 이미 사용 중이라는 에러
```
Error: bind: address already in use
```

**해결방법:**
```bash
# 포트 사용 중인 프로세스 확인
sudo lsof -i :5000
sudo lsof -i :5432

# 프로세스 종료
sudo kill -9 <PID>
```

### Docker 메모리 부족
**증상:** 컨테이너가 자꾸 재시작됨

**해결방법:**
```bash
# Docker Desktop 설정에서 메모리 증가
# Settings → Resources → Memory: 최소 4GB 권장
```

### Elasticsearch 시작 실패
**증상:** Elasticsearch 컨테이너가 시작되지 않음

**해결방법:**
```bash
# vm.max_map_count 증가 (Linux/Mac)
sudo sysctl -w vm.max_map_count=262144

# 영구 설정
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

### 데이터베이스 연결 실패
**증상:** API 서버에서 DB 연결 실패

**해결방법:**
```bash
# PostgreSQL 로그 확인
docker-compose logs database

# 컨테이너 재시작
docker-compose restart database api-server
```

---

## 📈 성능 최적화 팁

### 1. 로컬 개발 시
```yaml
# docker-compose.override.yml 생성
services:
  api-server:
    command: flask run --debug
    volumes:
      - ./:/app
```

### 2. 프로덕션 배포 시
- Gunicorn worker 수 증가: `workers=4`
- PostgreSQL connection pool 설정
- Redis maxmemory 정책 설정
- Nginx 리버스 프록시 추가

### 3. 모니터링 최적화
- Prometheus 스크랩 간격 조정 (기본 15초)
- Grafana 대시보드 새로고침 간격 설정
- Elasticsearch 인덱스 수명 주기 정책 설정

---

## 📚 추가 문서

- [API.md](../docs/API.md) - REST API 전체 문서
- [DEPLOYMENT.md](../docs/DEPLOYMENT.md) - 배포 가이드
- [README.md](../README.md) - 프로젝트 개요
- [docker-compose.yml](../docker-compose.yml) - 서비스 구성

---

## 🤝 기여

버그 리포트, 기능 제안, Pull Request 환영합니다!

---

## 📝 라이선스

MIT License

---

**마지막 업데이트:** 2025-11-17
**버전:** 1.0.0
