# 💾 데이터베이스 & 파일 처리

이 폴더에는 데이터베이스 운영 및 파일 처리를 위한 10개의 프로그램이 포함되어 있습니다.

> **📚 전체 사용 설명서**: 상세한 한글 가이드는 [사용설명서.md](./사용설명서.md)를 참조하세요.

## 📋 프로그램 목록

### 21. SQLite 데이터베이스
**파일**: `21_sqlite_database.py`

완전한 SQLite 데이터베이스 관리 시스템입니다.

**주요 기능**:
- 테이블 생성 및 관리
- CRUD 연산
- JOIN 및 복잡한 쿼리
- 백업 및 복원
- JSON 내보내기

**실행 방법**:
```bash
python 21_sqlite_database.py
```

**사용 예시**:
```python
from sqlite_database import UserDatabase

db = UserDatabase()
# 사용자 추가
user_id = db.create_user("홍길동", "hong@example.com", "password123")
# 사용자 조회
user = db.get_user(user_id)
print(f"사용자: {user['username']}, 이메일: {user['email']}")
```

**트랜잭션 처리**:
```python
db.begin_transaction()
try:
    db.create_user("user1", "user1@example.com", "pass1")
    db.create_user("user2", "user2@example.com", "pass2")
    db.commit()
except Exception as e:
    db.rollback()
    print(f"에러: {e}")
```

---

### 22. CSV 핸들러
**파일**: `22_csv_handler.py`

고급 CSV 파일 처리 도구입니다.

**주요 기능**:
- CSV 읽기/쓰기
- 필터링 및 정렬
- 통계 계산
- 그룹화 연산
- JSON 변환

**실행 방법**:
```bash
python 22_csv_handler.py
```

**대용량 CSV 처리**:
```python
from csv_handler import CSVHandler

handler = CSVHandler()
# 대용량 파일을 청크 단위로 처리
for chunk in handler.read_large_csv('large_file.csv', chunksize=1000):
    processed = handler.process_chunk(chunk)
    handler.save_chunk(processed, 'output.csv')
```

**데이터 분석**:
```python
# CSV 통계
stats = handler.get_statistics('sales.csv', column='revenue')
print(f"평균: {stats['mean']}, 합계: {stats['sum']}")

# 그룹별 집계
grouped = handler.group_by('sales.csv', group_column='category', agg_column='revenue')
```

---

### 23. JSON 프로세서
**파일**: `23_json_processor.py`

JSON 파싱 및 조작 도구입니다.

**주요 기능**:
- JSON 로드/저장
- 경로 기반 접근
- 검색 및 필터링
- 병합 및 평탄화
- 스키마 검증
- CSV 변환

**실행 방법**:
```bash
python 23_json_processor.py
```

**중첩 JSON 탐색**:
```python
from json_processor import JSONProcessor

jp = JSONProcessor()
data = jp.load('config.json')

# 경로 기반 접근
value = jp.get_path(data, 'database.connection.host')
print(f"DB 호스트: {value}")

# 스키마 검증
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"}
    },
    "required": ["name", "age"]
}
is_valid = jp.validate_schema(data, schema)
```

---

### 24. XML 파서
**파일**: `24_xml_parser.py`

XML 파일 파싱 및 생성 도구입니다.

**주요 기능**:
- XML 파일 파싱
- 요소 검색
- 속성 처리
- 딕셔너리 변환
- XML 생성

**실행 방법**:
```bash
python 24_xml_parser.py
```

**XML to Dict 변환**:
```python
from xml_parser import XMLParser

parser = XMLParser()
# XML 파일을 딕셔너리로 변환
data = parser.parse_file('config.xml')
print(data)

# 특정 요소 검색
elements = parser.find_elements('config.xml', tag='database')
for elem in elements:
    print(f"Database: {elem.get('name')}")
```

---

### 25. 로그 분석기
**파일**: `25_log_analyzer.py`

로그 파일 분석 및 리포팅 도구입니다.

**주요 기능**:
- Apache/Nginx 로그 파싱
- 상태 코드 분석
- IP 추적
- 대역폭 계산
- 인기 엔드포인트

**실행 방법**:
```bash
python 25_log_analyzer.py
```

**로그 분석 예시**:
```python
from log_analyzer import LogAnalyzer

analyzer = LogAnalyzer()
# 로그 파일 분석
stats = analyzer.analyze('access.log')

print(f"총 요청: {stats['total_requests']}")
print(f"고유 IP: {stats['unique_ips']}")
print(f"에러율: {stats['error_rate']}%")

# 상위 엔드포인트
top_endpoints = analyzer.get_top_endpoints('access.log', n=10)
for endpoint, count in top_endpoints:
    print(f"{endpoint}: {count}회")
```

**실시간 모니터링**:
```python
# 실시간 로그 모니터링
for entry in analyzer.tail_log('access.log'):
    if entry['status'] >= 400:
        print(f"에러 감지: {entry['ip']} - {entry['endpoint']}")
```

---

### 26. 파일 정리 도구
**파일**: `26_file_organizer.py`

자동 파일 정리 도구입니다.

**주요 기능**:
- 파일 형식별 정리
- 날짜별 정리
- 중복 제거
- 일괄 이름 변경
- 통계

**실행 방법**:
```bash
python 26_file_organizer.py
```

**파일 정리 예시**:
```python
from file_organizer import FileOrganizer

organizer = FileOrganizer()

# 확장자별 정리
organizer.organize_by_type('/path/to/downloads')
# 결과: /downloads/images/, /downloads/documents/, /downloads/videos/

# 중복 파일 제거
duplicates = organizer.find_duplicates('/path/to/folder')
print(f"중복 파일 {len(duplicates)}개 발견")
organizer.remove_duplicates(duplicates, keep='newest')
```

---

### 27. 마크다운 변환기
**파일**: `27_markdown_converter.py`

마크다운을 HTML로 변환하는 도구입니다.

**주요 기능**:
- 헤더, 리스트, 코드 블록
- 굵게, 기울임, 링크
- 이미지 및 인용
- 문법 강조
- 완전한 HTML 출력

**실행 방법**:
```bash
python 27_markdown_converter.py
```

**변환 예시**:
```python
from markdown_converter import MarkdownConverter

converter = MarkdownConverter()

markdown = """
# 제목
## 부제목

- 항목 1
- 항목 2

**굵은 글씨** 및 *기울임*

[링크](https://example.com)
"""

html = converter.convert(markdown)
converter.save_html(html, 'output.html')
```

---

### 28. 캐싱 시스템
**파일**: `28_caching_system.py`

LRU 캐시 및 메모이제이션 시스템입니다.

**주요 기능**:
- 메모리 캐시
- 파일 캐시
- LRU 제거 정책
- TTL 지원
- 메모이제이션 데코레이터

**실행 방법**:
```bash
python 28_caching_system.py
```

**캐시 사용**:
```python
from caching_system import LRUCache, memoize

# LRU 캐시
cache = LRUCache(capacity=100)
cache.put('user:1', {'name': '홍길동', 'email': 'hong@example.com'})
user = cache.get('user:1')

# 메모이제이션
@memoize(ttl=300)  # 5분 캐시
def expensive_calculation(n):
    return sum(range(n))

result = expensive_calculation(1000000)  # 첫 호출: 계산
result = expensive_calculation(1000000)  # 두 번째 호출: 캐시에서 반환
```

---

### 29. 속도 제한기
**파일**: `29_rate_limiter.py`

API 속도 제한 알고리즘입니다.

**알고리즘**:
- 토큰 버킷
- 슬라이딩 윈도우 로그
- 고정 윈도우
- 누출 버킷
- 다중 사용자 지원

**실행 방법**:
```bash
python 29_rate_limiter.py
```

**API 속도 제한**:
```python
from rate_limiter import TokenBucket, RateLimiter

# 토큰 버킷 (초당 10개 요청)
limiter = TokenBucket(capacity=10, refill_rate=10)

for request in incoming_requests:
    if limiter.allow():
        process_request(request)
    else:
        return "429 Too Many Requests"

# 사용자별 속도 제한
rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)

if rate_limiter.is_allowed(user_id='user123'):
    process_api_call()
else:
    return "Rate limit exceeded"
```

---

### 30. 작업 스케줄러
**파일**: `30_task_scheduler.py`

작업 스케줄링 시스템입니다.

**주요 기능**:
- 간격 기반 작업
- 시간 기반 작업
- 일회성 작업
- 우선순위 스케줄링
- 스레드 풀

**실행 방법**:
```bash
python 30_task_scheduler.py
```

**작업 스케줄링**:
```python
from task_scheduler import TaskScheduler

scheduler = TaskScheduler()

# 5분마다 실행
@scheduler.interval(minutes=5)
def backup_database():
    print("데이터베이스 백업 중...")

# 매일 오전 9시 실행
@scheduler.daily(hour=9, minute=0)
def send_daily_report():
    print("일일 리포트 발송 중...")

# 일회성 작업 (10초 후 실행)
@scheduler.once(delay=10)
def cleanup():
    print("임시 파일 정리 중...")

scheduler.start()
```

---

## ⚡ 빠른 시작

### 1. 의존성 설치
```bash
pip install pandas lxml
```

### 2. 첫 번째 프로그램 실행
```bash
cd 03_database_file_processing
python 21_sqlite_database.py
```

### 3. 데이터베이스 테스트
```python
from sqlite_database import UserDatabase

db = UserDatabase()
user_id = db.create_user("테스트사용자", "test@example.com", "password")
print(f"사용자 생성 완료: ID {user_id}")
```

## 🔧 문제 해결

### SQLite 잠금 에러
```python
# 타임아웃 증가
import sqlite3
conn = sqlite3.connect('database.db', timeout=30.0)
```

### CSV 인코딩 문제
```python
# UTF-8로 읽기
import pandas as pd
df = pd.read_csv('file.csv', encoding='utf-8-sig')

# 인코딩 자동 감지
import chardet
with open('file.csv', 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']
```

### 대용량 파일 처리
```python
# 청크 단위 처리
chunksize = 10000
for chunk in pd.read_csv('large_file.csv', chunksize=chunksize):
    process(chunk)
```

### JSON 인코딩 에러
```python
import json

# ensure_ascii=False로 한글 지원
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## 📚 실전 활용 예시

### 1. 사용자 관리 시스템
```python
from sqlite_database import UserDatabase

class UserManagement:
    def __init__(self):
        self.db = UserDatabase()

    def register(self, username, email, password):
        # 이메일 중복 체크
        if self.db.email_exists(email):
            return {"error": "이메일이 이미 존재합니다"}

        # 사용자 생성
        user_id = self.db.create_user(username, email, password)
        return {"success": True, "user_id": user_id}

    def login(self, email, password):
        user = self.db.authenticate(email, password)
        if user:
            return {"success": True, "user": user}
        return {"error": "인증 실패"}
```

### 2. 판매 데이터 분석
```python
from csv_handler import CSVHandler

handler = CSVHandler()

# 월별 판매 집계
monthly_sales = handler.group_by(
    'sales.csv',
    group_column='month',
    agg_column='revenue',
    agg_func='sum'
)

# 상위 제품
top_products = handler.sort_by('sales.csv', column='units_sold', ascending=False)
print(top_products.head(10))
```

### 3. 설정 관리 시스템
```python
from json_processor import JSONProcessor

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.jp = JSONProcessor()
        self.config = self.jp.load(config_file)

    def get(self, path, default=None):
        return self.jp.get_path(self.config, path, default)

    def set(self, path, value):
        self.jp.set_path(self.config, path, value)
        self.jp.save(self.config, self.config_file)

# 사용 예시
config = ConfigManager()
db_host = config.get('database.host', 'localhost')
config.set('database.port', 5432)
```

## 📊 지원 파일 형식

| 형식 | 프로그램 | 용도 |
|------|---------|------|
| SQLite | 21 | 관계형 데이터베이스 |
| CSV | 22 | 표 형식 데이터 |
| JSON | 23 | 구조화된 데이터 |
| XML | 24 | 계층적 데이터 |
| 로그 | 25 | 서버 로그 분석 |
| Markdown | 27 | 문서 변환 |

## 🎯 학습 경로

### 초급
1. CSV 핸들러 (22)
2. JSON 프로세서 (23)
3. 파일 정리 도구 (26)

### 중급
4. SQLite 데이터베이스 (21)
5. 로그 분석기 (25)
6. 마크다운 변환기 (27)
7. 캐싱 시스템 (28)

### 고급
8. XML 파서 (24)
9. 속도 제한기 (29)
10. 작업 스케줄러 (30)

## 🌟 추천 실습 프로젝트

1. **데이터 파이프라인** (프로그램 22 + 23 + 21)
   - CSV → JSON 변환 → SQLite 저장

2. **로그 모니터링 시스템** (프로그램 25 + 30)
   - 실시간 로그 분석 + 알림 스케줄링

3. **파일 백업 시스템** (프로그램 26 + 28 + 30)
   - 자동 정리 + 캐싱 + 스케줄링

## 📖 상세 가이드

각 프로그램의 상세한 실전 활용법, 예제 코드, 모범 사례는 **[사용설명서.md](./사용설명서.md)**를 참조하세요.

사용설명서에는 다음 내용이 포함되어 있습니다:
- 🎯 실전 활용 시나리오
- 💡 상세한 코드 예제
- 🏆 모범 사례 및 팁
- 🔍 성능 최적화 방법
- 🚀 대용량 데이터 처리 기법

---

**총 프로그램 수**: 10개 | **카테고리**: 데이터베이스 & 파일 처리

**도움이 필요하신가요?** [사용설명서.md](./사용설명서.md)를 확인하거나 이슈를 등록해 주세요!
