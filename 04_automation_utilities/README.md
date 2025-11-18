# 🤖 자동화 & 유틸리티

이 폴더에는 자동화 및 유틸리티 10개의 프로그램이 포함되어 있습니다.

> **📚 전체 사용 설명서**: 상세한 한글 가이드는 [사용설명서.md](./사용설명서.md)를 참조하세요.

## 📋 프로그램 목록

### 31. 웹 자동화
**파일**: `31_web_automation.py`

Selenium 기반 웹 자동화 프레임워크입니다.

**주요 기능**:
- 브라우저 자동화
- 요소 상호작용
- 폼 자동 채우기
- 스크린샷
- JavaScript 실행

**실행 방법**:
```bash
pip install selenium
python 31_web_automation.py
```

**로그인 자동화 예시**:
```python
from web_automation import WebAutomation

auto = WebAutomation()
auto.navigate_to("https://example.com/login")
auto.fill_form({
    "username": "user@example.com",
    "password": "password123"
})
auto.click_button("로그인")
auto.take_screenshot("login_success.png")
```

**데이터 수집 자동화**:
```python
# E-commerce 제품 정보 수집
products = []
for page in range(1, 10):
    auto.navigate_to(f"https://example.com/products?page={page}")
    items = auto.find_elements(".product-item")
    for item in items:
        name = item.find_element(".product-name").text
        price = item.find_element(".product-price").text
        products.append({"name": name, "price": price})
```

---

### 32. PDF 생성기
**파일**: `32_pdf_generator.py`

ReportLab 기반 PDF 생성 도구입니다.

**주요 기능**:
- 텍스트 및 단락
- 표와 차트
- 이미지
- 헤더 및 푸터
- 커스텀 스타일링

**실행 방법**:
```bash
pip install reportlab
python 32_pdf_generator.py
```

**보고서 생성**:
```python
from pdf_generator import PDFGenerator

pdf = PDFGenerator()
pdf.add_title("월간 판매 보고서")
pdf.add_text("2024년 1월 판매 실적")

# 표 추가
data = [
    ["제품", "판매량", "매출"],
    ["제품 A", "100", "1,000,000"],
    ["제품 B", "150", "1,500,000"]
]
pdf.add_table(data)

# 차트 추가
pdf.add_chart([100, 150, 200], title="월별 판매 추이")

pdf.save("sales_report.pdf")
```

**송장 생성**:
```python
invoice_data = {
    "invoice_number": "INV-2024-001",
    "customer": "홍길동",
    "items": [
        {"name": "상품1", "qty": 2, "price": 50000},
        {"name": "상품2", "qty": 1, "price": 30000}
    ],
    "total": 130000
}
pdf.generate_invoice(invoice_data, "invoice_001.pdf")
```

---

### 33. CLI 도구
**파일**: `33_cli_tool.py`

명령줄 인터페이스 프레임워크입니다.

**주요 기능**:
- 인자 파싱
- 서브커맨드
- 진행률 표시줄
- 표 출력
- 컬러 지원

**실행 방법**:
```bash
python 33_cli_tool.py hello --name Alice
python 33_cli_tool.py list --format table
```

**CLI 도구 만들기**:
```python
import click
from rich.console import Console
from rich.table import Table

@click.group()
def cli():
    """프로젝트 관리 도구"""
    pass

@cli.command()
@click.option('--name', prompt='프로젝트 이름', help='프로젝트 이름')
def create(name):
    """새 프로젝트 생성"""
    console = Console()
    with console.status(f"[bold green]{name} 프로젝트 생성 중..."):
        # 프로젝트 생성 로직
        time.sleep(2)
    console.print(f"[green]✓[/green] {name} 프로젝트가 생성되었습니다!")

@cli.command()
def list():
    """프로젝트 목록 표시"""
    table = Table(title="프로젝트 목록")
    table.add_column("이름", style="cyan")
    table.add_column("상태", style="magenta")
    table.add_row("프로젝트A", "활성")
    table.add_row("프로젝트B", "비활성")

    console = Console()
    console.print(table)

if __name__ == '__main__':
    cli()
```

---

### 34. 설정 관리자
**파일**: `34_config_manager.py`

다중 형식 설정 관리자입니다.

**형식 지원**:
- JSON
- INI
- 환경 변수
- 중첩 키
- 기본값

**실행 방법**:
```bash
python 34_config_manager.py
```

**설정 관리**:
```python
from config_manager import ConfigManager

config = ConfigManager('config.json')

# 값 가져오기
db_host = config.get('database.host', default='localhost')
db_port = config.get('database.port', default=5432)

# 값 설정
config.set('database.host', 'db.example.com')
config.set('database.credentials.username', 'admin')

# 환경 변수 우선순위
# DATABASE_HOST 환경 변수가 있으면 우선 사용
host = config.get('database.host', env_var='DATABASE_HOST')
```

---

### 35. QR 코드 생성기
**파일**: `35_qr_code_generator.py`

QR 코드 생성 및 스캔 도구입니다.

**주요 기능**:
- 기본 QR 코드
- 컬러 QR 코드
- 로고 포함 QR 코드
- WiFi QR 코드
- vCard QR 코드

**실행 방법**:
```bash
pip install qrcode[pil]
python 35_qr_code_generator.py
```

**QR 코드 생성**:
```python
from qr_code_generator import QRCodeGenerator

qr = QRCodeGenerator()

# 기본 QR 코드
qr.generate("https://example.com", "website.png")

# WiFi QR 코드
qr.generate_wifi(
    ssid="MyWiFi",
    password="password123",
    security="WPA",
    filename="wifi_qr.png"
)

# 명함 QR 코드
vcard = {
    "name": "홍길동",
    "phone": "010-1234-5678",
    "email": "hong@example.com",
    "url": "https://example.com"
}
qr.generate_vcard(vcard, "business_card.png")
```

---

### 36. 텍스트 음성 변환
**파일**: `36_text_to_speech.py`

다중 음성 TTS 엔진입니다.

**주요 기능**:
- 오프라인 TTS (pyttsx3)
- 온라인 TTS (Google)
- 다국어 지원
- 음성 선택
- 파일 저장

**실행 방법**:
```bash
pip install pyttsx3 gtts
python 36_text_to_speech.py
```

**음성 변환**:
```python
from text_to_speech import TextToSpeech

tts = TextToSpeech()

# 한국어 음성 변환
tts.speak("안녕하세요, 반갑습니다!", lang='ko')

# 파일로 저장
tts.save_to_file("중요한 공지사항입니다.", "announcement.mp3", lang='ko')

# 영어 음성
tts.speak("Hello, World!", lang='en')
```

**긴 텍스트 읽기**:
```python
with open('article.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    tts.save_to_file(text, "article_audio.mp3", lang='ko')
```

---

### 37. 백업 도구
**파일**: `37_backup_tool.py`

파일 백업 및 복원 시스템입니다.

**주요 기능**:
- ZIP 백업
- TAR 백업
- 증분 백업
- 복원 기능
- 백업 로테이션

**실행 방법**:
```bash
python 37_backup_tool.py
```

**백업 생성**:
```python
from backup_tool import BackupTool

backup = BackupTool()

# 전체 백업
backup.create_full_backup(
    source='/path/to/project',
    destination='/path/to/backups',
    name='project_backup'
)

# 증분 백업 (변경된 파일만)
backup.create_incremental_backup(
    source='/path/to/project',
    destination='/path/to/backups',
    base_backup='project_backup_20240101.zip'
)

# 백업 복원
backup.restore(
    backup_file='/path/to/backups/project_backup_20240101.zip',
    destination='/path/to/restore'
)
```

**자동 백업 스케줄링**:
```python
import schedule

def daily_backup():
    backup.create_full_backup(
        source='/important/data',
        destination='/backups',
        name=f'daily_backup_{datetime.now().strftime("%Y%m%d")}'
    )
    # 7일 이상 된 백업 삭제
    backup.cleanup_old_backups('/backups', days=7)

schedule.every().day.at("02:00").do(daily_backup)
```

---

### 38. 시스템 모니터
**파일**: `38_system_monitor.py`

실시간 시스템 리소스 모니터링 도구입니다.

**모니터링 항목**:
- CPU 사용률
- 메모리 사용률
- 디스크 사용률
- 네트워크 I/O
- 프로세스 목록
- 배터리 상태

**실행 방법**:
```bash
pip install psutil
python 38_system_monitor.py
```

**시스템 모니터링**:
```python
from system_monitor import SystemMonitor

monitor = SystemMonitor()

# 실시간 모니터링
while True:
    stats = monitor.get_stats()
    print(f"CPU: {stats['cpu_percent']}%")
    print(f"메모리: {stats['memory_percent']}%")
    print(f"디스크: {stats['disk_percent']}%")

    # CPU 사용률이 80% 초과 시 알림
    if stats['cpu_percent'] > 80:
        send_alert(f"CPU 사용률 높음: {stats['cpu_percent']}%")

    time.sleep(5)
```

**프로세스 관리**:
```python
# 메모리 사용량 상위 10개 프로세스
top_processes = monitor.get_top_processes(by='memory', n=10)
for proc in top_processes:
    print(f"{proc['name']}: {proc['memory_mb']}MB")

# 특정 프로세스 종료
monitor.kill_process_by_name('chrome.exe')
```

---

### 39. 알림 시스템
**파일**: `39_notification_system.py`

다중 채널 알림 시스템입니다.

**채널**:
- 데스크톱 알림
- 이메일
- Slack
- 조건 기반 알림
- 알림 로그

**실행 방법**:
```bash
pip install win10toast  # Windows용
python 39_notification_system.py
```

**알림 전송**:
```python
from notification_system import NotificationSystem

notifier = NotificationSystem()

# 데스크톱 알림
notifier.desktop("백업 완료", "데이터베이스 백업이 성공적으로 완료되었습니다.")

# 이메일 알림
notifier.email(
    to="admin@example.com",
    subject="시스템 알림",
    body="CPU 사용률이 90%를 초과했습니다."
)

# Slack 알림
notifier.slack(
    webhook_url="https://hooks.slack.com/services/...",
    message="배포가 완료되었습니다.",
    channel="#deployments"
)
```

**조건 기반 알림**:
```python
# 시스템 모니터링 + 알림
from system_monitor import SystemMonitor

monitor = SystemMonitor()
notifier = NotificationSystem()

def check_and_alert():
    stats = monitor.get_stats()

    if stats['cpu_percent'] > 80:
        notifier.desktop("CPU 경고", f"CPU 사용률: {stats['cpu_percent']}%")
        notifier.email(
            to="admin@example.com",
            subject="CPU 사용률 경고",
            body=f"현재 CPU 사용률: {stats['cpu_percent']}%"
        )

    if stats['disk_percent'] > 90:
        notifier.slack(
            webhook_url=SLACK_WEBHOOK,
            message=f"⚠️ 디스크 공간 부족: {stats['disk_percent']}%"
        )
```

---

### 40. API 클라이언트
**파일**: `40_api_client.py`

REST API 클라이언트 라이브러리입니다.

**주요 기능**:
- GET, POST, PUT, DELETE
- 인증
- 캐싱
- 속도 제한
- 재시도 로직
- 예제: GitHub API

**실행 방법**:
```bash
pip install requests
python 40_api_client.py
```

**API 클라이언트 사용**:
```python
from api_client import APIClient

# GitHub API 클라이언트
client = APIClient(
    base_url="https://api.github.com",
    auth_token="your_github_token"
)

# GET 요청
user = client.get("/user")
print(f"사용자: {user['login']}")

# 저장소 목록
repos = client.get("/user/repos")
for repo in repos:
    print(f"- {repo['name']}: {repo['stargazers_count']} stars")

# POST 요청 (새 이슈 생성)
issue = client.post("/repos/owner/repo/issues", data={
    "title": "버그 리포트",
    "body": "버그 설명..."
})
```

**재시도 및 캐싱**:
```python
# 자동 재시도 (네트워크 에러 시)
client = APIClient(
    base_url="https://api.example.com",
    max_retries=3,
    backoff_factor=2  # 2초, 4초, 8초 대기
)

# 응답 캐싱 (60초)
@client.cache(ttl=60)
def get_user_profile(user_id):
    return client.get(f"/users/{user_id}")

# 첫 호출: API 요청
profile = get_user_profile(123)

# 두 번째 호출 (60초 이내): 캐시에서 반환
profile = get_user_profile(123)
```

---

## ⚡ 빠른 시작

### 1. 의존성 설치
```bash
pip install selenium reportlab qrcode pyttsx3 gtts psutil requests win10toast click rich
```

또는:
```bash
pip install -r requirements.txt
```

### 2. 첫 번째 프로그램 실행
```bash
cd 04_automation_utilities
python 38_system_monitor.py
```

## 🔧 문제 해결

### Selenium WebDriver 설치
```bash
# Chrome WebDriver
# 1. Chrome 버전 확인 (chrome://version)
# 2. https://chromedriver.chromium.org/ 에서 다운로드
# 3. PATH에 추가 또는 스크립트와 같은 폴더에 위치

# 또는 webdriver-manager 사용
pip install webdriver-manager

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

### PDF 한글 폰트 문제
```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 한글 폰트 등록
pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

# 사용
canvas.setFont('NanumGothic', 12)
```

### TTS 음성 언어 설정
```python
# Windows에서 한국어 음성 확인
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.name)
```

### psutil 권한 오류
```bash
# Linux/Mac에서 일부 기능은 root 권한 필요
sudo python 38_system_monitor.py
```

## 📚 실전 활용 예시

### 1. 자동 리포트 생성 시스템
```python
from system_monitor import SystemMonitor
from pdf_generator import PDFGenerator
from notification_system import NotificationSystem

def generate_daily_report():
    # 시스템 통계 수집
    monitor = SystemMonitor()
    stats = monitor.get_daily_stats()

    # PDF 리포트 생성
    pdf = PDFGenerator()
    pdf.add_title("일일 시스템 리포트")
    pdf.add_table([
        ["항목", "평균", "최대"],
        ["CPU", f"{stats['cpu_avg']}%", f"{stats['cpu_max']}%"],
        ["메모리", f"{stats['mem_avg']}%", f"{stats['mem_max']}%"]
    ])
    pdf.save("daily_report.pdf")

    # 이메일 전송
    notifier = NotificationSystem()
    notifier.email_with_attachment(
        to="admin@example.com",
        subject="일일 시스템 리포트",
        body="첨부된 리포트를 확인하세요.",
        attachment="daily_report.pdf"
    )
```

### 2. E2E 테스트 자동화
```python
from web_automation import WebAutomation

def test_checkout_process():
    auto = WebAutomation()

    # 로그인
    auto.navigate_to("https://shop.example.com")
    auto.login("test@example.com", "password")

    # 상품 검색 및 추가
    auto.search("노트북")
    auto.click(".product-item:first-child")
    auto.click("#add-to-cart")

    # 결제
    auto.navigate_to("/cart")
    auto.click("#checkout")
    auto.fill_shipping_info({
        "name": "홍길동",
        "address": "서울시 강남구...",
        "phone": "010-1234-5678"
    })

    # 검증
    assert "주문 완료" in auto.get_page_text()
    auto.take_screenshot("checkout_success.png")
```

### 3. 종합 모니터링 대시보드
```python
import schedule
from system_monitor import SystemMonitor
from notification_system import NotificationSystem
from api_client import APIClient

monitor = SystemMonitor()
notifier = NotificationSystem()

def check_system_health():
    stats = monitor.get_stats()

    # 임계값 체크
    alerts = []
    if stats['cpu_percent'] > 80:
        alerts.append(f"⚠️ CPU: {stats['cpu_percent']}%")
    if stats['memory_percent'] > 85:
        alerts.append(f"⚠️ 메모리: {stats['memory_percent']}%")
    if stats['disk_percent'] > 90:
        alerts.append(f"🔴 디스크: {stats['disk_percent']}%")

    if alerts:
        notifier.slack(
            webhook_url=SLACK_WEBHOOK,
            message="\n".join(alerts)
        )

# 5분마다 체크
schedule.every(5).minutes.do(check_system_health)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 🎯 학습 경로

### 초급
1. QR 코드 생성기 (35)
2. 텍스트 음성 변환 (36)
3. 설정 관리자 (34)

### 중급
4. 시스템 모니터 (38)
5. CLI 도구 (33)
6. PDF 생성기 (32)
7. 백업 도구 (37)

### 고급
8. 웹 자동화 (31)
9. 알림 시스템 (39)
10. API 클라이언트 (40)

## 🌟 추천 실습 프로젝트

1. **자동 배포 시스템** (프로그램 31 + 37 + 39)
   - 웹 자동화로 배포 + 백업 + Slack 알림

2. **시스템 관리 봇** (프로그램 38 + 39 + 40)
   - 모니터링 + 알림 + API 통합

3. **문서 자동화** (프로그램 32 + 33 + 36)
   - PDF 리포트 생성 + CLI 도구 + TTS

## 📖 상세 가이드

각 프로그램의 상세한 실전 활용법, 예제 코드, 모범 사례는 **[사용설명서.md](./사용설명서.md)**를 참조하세요.

사용설명서에는 다음 내용이 포함되어 있습니다:
- 🎯 실전 활용 시나리오
- 💡 상세한 코드 예제
- 🏆 모범 사례 및 팁
- 🔍 일반적인 문제 해결
- 🚀 고급 자동화 기법

---

**총 프로그램 수**: 10개 | **카테고리**: 자동화 & 유틸리티

**도움이 필요하신가요?** [사용설명서.md](./사용설명서.md)를 확인하거나 이슈를 등록해 주세요!
