# 🌐 Web & API 예제

이 폴더에는 웹 및 API 관련 10개의 완전한 Python 프로그램이 포함되어 있습니다.

> **📚 전체 사용 설명서**: 상세한 한글 가이드는 [사용설명서.md](./사용설명서.md)를 참조하세요.

## 📋 프로그램 목록

### 01. REST API 서버
**파일**: `01_rest_api_server.py`

Flask 기반의 완전한 CRUD 기능을 갖춘 작업 관리 REST API 서버입니다.

**주요 기능**:
- GET, POST, PUT, DELETE 엔드포인트
- 메모리 기반 데이터베이스
- JSON 응답
- 에러 핸들링

**실행 방법**:
```bash
python 01_rest_api_server.py
# http://localhost:5000 에서 접속
```

**빠른 테스트**:
```bash
# 작업 목록 조회
curl http://localhost:5000/tasks

# 새 작업 추가
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"테스트 작업","description":"테스트 설명"}'
```

---

### 02. 웹 스크레이퍼
**파일**: `02_web_scraper.py`

BeautifulSoup 기반의 웹 스크래핑 도구입니다.

**주요 기능**:
- 링크, 이미지, 텍스트 추출
- JSON 파일로 결과 저장
- 에러 핸들링
- 커스터마이징 가능한 선택자

**실행 방법**:
```bash
python 02_web_scraper.py
```

**사용 예시**:
```python
from web_scraper import WebScraper

scraper = WebScraper()
results = scraper.scrape("https://example.com")
print(f"발견된 링크 수: {len(results['links'])}")
```

---

### 03. 데이터 시각화
**파일**: `03_data_visualization.py`

Matplotlib 기반의 데이터 시각화 툴킷입니다.

**주요 기능**:
- 선 그래프
- 막대 그래프
- 파이 차트
- 산점도
- 히스토그램

**실행 방법**:
```bash
python 03_data_visualization.py
```

---

### 04. JWT 인증
**파일**: `04_jwt_authentication.py`

JWT 토큰 기반 인증 시스템입니다.

**주요 기능**:
- 사용자 로그인/인증
- 토큰 생성 및 검증
- 역할 기반 접근 제어
- 보호된 라우트

**실행 방법**:
```bash
python 04_jwt_authentication.py
# 테스트 계정: admin/admin123 또는 user/user123
```

**API 테스트**:
```bash
# 로그인
curl -X POST http://localhost:5001/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 보호된 리소스 접근 (토큰 필요)
curl http://localhost:5001/protected \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

### 05. 이메일 발송
**파일**: `05_email_sender.py`

SMTP 기반 이메일 발송 시스템입니다.

**주요 기능**:
- 텍스트 이메일
- HTML 이메일
- 첨부 파일
- 대량 발송

**실행 방법**:
```bash
# 먼저 SMTP 설정을 구성하세요
python 05_email_sender.py
```

**환경 변수 설정**:
```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
```

---

### 06. 파일 암호화
**파일**: `06_file_encryption.py`

Cryptography 라이브러리 기반의 파일 암호화/복호화 도구입니다.

**주요 기능**:
- 파일 암호화
- 파일 복호화
- 비밀번호 기반 키
- 텍스트 암호화

**실행 방법**:
```bash
python 06_file_encryption.py
```

**사용 예시**:
```python
from file_encryption import FileEncryption

fe = FileEncryption()
# 파일 암호화
fe.encrypt_file("secret.txt", "mypassword")
# 복호화
fe.decrypt_file("secret.txt.enc", "mypassword", "secret_decrypted.txt")
```

---

### 07. 이미지 처리
**파일**: `07_image_processor.py`

PIL/Pillow 기반의 이미지 처리 도구입니다.

**주요 기능**:
- 크기 조정, 회전, 뒤집기
- 필터 (블러, 샤프)
- 밝기/대비 조정
- 워터마크
- 썸네일 생성

**실행 방법**:
```bash
python 07_image_processor.py
```

---

### 08. 챗봇
**파일**: `08_chatbot.py`

규칙 기반 대화형 챗봇입니다.

**주요 기능**:
- 패턴 매칭
- 대화 기록
- 다양한 응답 패턴
- 파일 저장

**실행 방법**:
```bash
python 08_chatbot.py
```

**대화 예시**:
```
You: 안녕
Bot: 안녕하세요! 무엇을 도와드릴까요?
You: 날씨가 어때?
Bot: 저는 날씨 정보를 제공할 수 없지만, 날씨 앱을 확인해보세요!
```

---

### 09. URL 단축기
**파일**: `09_url_shortener.py`

Flask 기반의 URL 단축 서비스입니다.

**주요 기능**:
- URL 단축
- 커스텀 단축 코드
- 클릭 추적
- SQLite 데이터베이스

**실행 방법**:
```bash
python 09_url_shortener.py
# http://localhost:5002 에서 접속
```

**API 사용**:
```bash
# URL 단축
curl -X POST http://localhost:5002/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/very/long/url"}'

# 단축 URL 접속
curl http://localhost:5002/abc123
```

---

### 10. 패스워드 관리자
**파일**: `10_password_manager.py`

암호화된 패스워드 관리 시스템입니다.

**주요 기능**:
- 마스터 비밀번호 보호
- 패스워드 생성
- 암호화된 저장소
- 패스워드 강도 검사

**실행 방법**:
```bash
python 10_password_manager.py
```

**사용 팁**:
- 마스터 비밀번호는 안전하게 보관하세요
- 강력한 비밀번호 생성기를 활용하세요
- 정기적으로 백업하세요

---

## ⚡ 빠른 시작

### 1. 의존성 설치
```bash
pip install flask requests beautifulsoup4 matplotlib pillow cryptography pyjwt
```

또는 프로젝트 루트의 requirements.txt 사용:
```bash
pip install -r requirements.txt
```

### 2. 첫 번째 프로그램 실행
```bash
cd 01_web_api
python 01_rest_api_server.py
```

### 3. API 테스트
브라우저에서 http://localhost:5000 접속 또는 curl 사용:
```bash
curl http://localhost:5000/tasks
```

## 🔧 문제 해결

### 포트가 이미 사용 중인 경우
```python
# 프로그램 내에서 포트 번호를 변경하세요
app.run(debug=True, port=5003)  # 다른 포트 번호 사용
```

### 모듈을 찾을 수 없는 경우
```bash
# 필요한 패키지 설치
pip install flask
pip install beautifulsoup4
pip install pillow
```

### SMTP 에러 (이메일 발송)
- Gmail 사용 시: "보안 수준이 낮은 앱 허용" 활성화 또는 앱 비밀번호 사용
- 방화벽이 SMTP 포트(587, 465)를 차단하지 않는지 확인

### 암호화 관련 에러
```bash
pip install cryptography
# Windows에서 빌드 도구가 필요할 수 있습니다
```

## 📚 실전 활용 가이드

각 프로그램의 상세한 실전 활용법, 예제 코드, 모범 사례는 **[사용설명서.md](./사용설명서.md)**를 참조하세요.

사용설명서에는 다음 내용이 포함되어 있습니다:
- 🎯 실전 활용 시나리오
- 💡 상세한 코드 예제
- 🏆 모범 사례 및 팁
- 🔍 일반적인 문제 해결
- 🚀 성능 최적화 방법

## 🎯 학습 경로

### 초급
1. REST API 서버 (01)
2. 웹 스크레이퍼 (02)
3. 챗봇 (08)

### 중급
4. JWT 인증 (04)
5. 파일 암호화 (06)
6. URL 단축기 (09)

### 고급
7. 이미지 처리 (07)
8. 데이터 시각화 (03)
9. 패스워드 관리자 (10)
10. 이메일 발송 시스템 (05)

## 📊 기술 스택

| 기술 | 용도 | 프로그램 |
|------|------|---------|
| Flask | 웹 프레임워크 | 01, 04, 09 |
| BeautifulSoup4 | 웹 스크래핑 | 02 |
| Matplotlib | 데이터 시각화 | 03 |
| JWT | 인증/인가 | 04 |
| SMTP | 이메일 발송 | 05 |
| Cryptography | 암호화 | 06, 10 |
| Pillow | 이미지 처리 | 07 |
| SQLite | 데이터베이스 | 09 |

## 🌟 추천 실습 프로젝트

1. **개인 블로그 API** (프로그램 01 + 04)
   - REST API 서버와 JWT 인증을 결합

2. **뉴스 수집기** (프로그램 02 + 05)
   - 웹 스크래핑으로 뉴스 수집 후 이메일 발송

3. **사진 관리 시스템** (프로그램 07 + 09)
   - 이미지 처리 및 URL 단축 기능 통합

---

**총 프로그램 수**: 10개 | **카테고리**: Web & API

**도움이 필요하신가요?** [사용설명서.md](./사용설명서.md)를 확인하거나 이슈를 등록해 주세요!
