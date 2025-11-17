"""
Load Testing with Locust
부하 테스트를 위한 Locust 설정
"""
from locust import HttpUser, task, between, events
import random
import json

class APIUser(HttpUser):
    """API 사용자 시뮬레이션"""

    wait_time = between(1, 3)  # 요청 간 대기 시간 (1-3초)

    def on_start(self):
        """테스트 시작 시 실행"""
        # JWT 토큰 획득
        response = self.client.post("http://localhost:5001/api/login",
            json={
                "username": "admin",
                "password": "admin123"
            },
            name="/api/login"
        )
        if response.status_code == 200:
            self.token = response.json().get('token')
        else:
            self.token = None

    @task(3)
    def get_all_tasks(self):
        """모든 작업 조회 (가중치: 3)"""
        self.client.get("/api/tasks", name="/api/tasks [GET]")

    @task(2)
    def create_task(self):
        """작업 생성 (가중치: 2)"""
        self.client.post("/api/tasks",
            json={
                "title": f"Load Test Task {random.randint(1, 10000)}",
                "description": "This is a load testing task",
                "completed": False
            },
            name="/api/tasks [POST]"
        )

    @task(2)
    def get_task_by_id(self):
        """특정 작업 조회 (가중치: 2)"""
        task_id = random.randint(1, 100)
        self.client.get(f"/api/tasks/{task_id}", name="/api/tasks/:id [GET]")

    @task(1)
    def update_task(self):
        """작업 업데이트 (가중치: 1)"""
        task_id = random.randint(1, 100)
        self.client.put(f"/api/tasks/{task_id}",
            json={"completed": True},
            name="/api/tasks/:id [PUT]"
        )

    @task(1)
    def delete_task(self):
        """작업 삭제 (가중치: 1)"""
        task_id = random.randint(1, 100)
        self.client.delete(f"/api/tasks/{task_id}", name="/api/tasks/:id [DELETE]")

    @task(1)
    def health_check(self):
        """헬스 체크 (가중치: 1)"""
        self.client.get("/api/health", name="/api/health")

    @task(1)
    def access_protected_route(self):
        """보호된 라우트 접근 (가중치: 1)"""
        if self.token:
            self.client.get("http://localhost:5001/api/protected",
                headers={"Authorization": f"Bearer {self.token}"},
                name="/api/protected [authenticated]"
            )

class AuthUser(HttpUser):
    """인증 사용자 시뮬레이션"""

    host = "http://localhost:5001"
    wait_time = between(2, 5)

    @task(5)
    def login(self):
        """로그인 (가중치: 5)"""
        username = random.choice(['admin', 'user'])
        password = f'{username}123'

        self.client.post("/api/login",
            json={"username": username, "password": password},
            name="/api/login"
        )

    @task(1)
    def invalid_login(self):
        """잘못된 로그인 시도 (가중치: 1)"""
        self.client.post("/api/login",
            json={"username": "hacker", "password": "wrong"},
            name="/api/login [invalid]"
        )

class StressTestUser(HttpUser):
    """스트레스 테스트 사용자"""

    wait_time = between(0.1, 0.5)  # 빠른 요청

    @task
    def rapid_health_checks(self):
        """빠른 헬스 체크"""
        self.client.get("/api/health")

# Locust 이벤트 핸들러
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("🚀 Load test starting...")
    print(f"Target: {environment.host}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("✅ Load test completed")
    print(f"Total requests: {environment.stats.total.num_requests}")
    print(f"Failed requests: {environment.stats.total.num_failures}")

# 사용 방법:
# locust -f tests/test_load.py --host=http://localhost:5000
#
# 웹 UI: http://localhost:8089
#
# Headless 모드:
# locust -f tests/test_load.py --host=http://localhost:5000 \
#        --users 100 --spawn-rate 10 --run-time 1m --headless
