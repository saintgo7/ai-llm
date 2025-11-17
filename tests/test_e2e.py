"""
End-to-End Tests - 전체 시스템의 종단 간 테스트
"""
import pytest
import requests
import time
import subprocess
import signal
import os
from contextlib import contextmanager

BASE_URL = os.getenv('TEST_BASE_URL', 'http://localhost:5000')
AUTH_URL = os.getenv('TEST_AUTH_URL', 'http://localhost:5001')

@contextmanager
def running_server(script_path, port):
    """테스트 서버 실행 컨텍스트 매니저"""
    process = subprocess.Popen(
        ['python', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # 서버 시작 대기
    time.sleep(2)

    try:
        yield process
    finally:
        # 프로세스 그룹 종료
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)

class TestEndToEnd:
    """종단 간 테스트"""

    @pytest.fixture(scope='class')
    def setup_servers(self):
        """테스트를 위한 서버 셋업"""
        # 실제 환경에서는 Docker Compose로 시작
        # 여기서는 서버가 이미 실행 중이라고 가정
        yield
        # Cleanup if needed

    def test_complete_user_journey(self, setup_servers):
        """완전한 사용자 여정 테스트"""

        # 1. 헬스 체크
        response = requests.get(f'{BASE_URL}/api/health')
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'

        # 2. 인증 (로그인)
        auth_response = requests.post(f'{AUTH_URL}/api/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        assert auth_response.status_code == 200
        token = auth_response.json()['token']

        # 3. 작업 생성 (여러 개)
        tasks = []
        for i in range(5):
            response = requests.post(f'{BASE_URL}/api/tasks', json={
                'title': f'E2E Task {i+1}',
                'description': f'End-to-end test task {i+1}',
                'completed': False
            })
            assert response.status_code == 201
            tasks.append(response.json())

        # 4. 모든 작업 조회
        response = requests.get(f'{BASE_URL}/api/tasks')
        assert response.status_code == 200
        data = response.json()
        assert data['count'] >= 5

        # 5. 필터링된 작업 조회
        response = requests.get(f'{BASE_URL}/api/tasks?status=pending')
        assert response.status_code == 200

        # 6. 작업 완료 처리
        for task in tasks[:3]:
            response = requests.put(f"{BASE_URL}/api/tasks/{task['id']}", json={
                'completed': True
            })
            assert response.status_code == 200

        # 7. 완료된 작업 조회
        response = requests.get(f'{BASE_URL}/api/tasks?status=completed')
        assert response.status_code == 200
        completed = response.json()
        assert completed['count'] >= 3

        # 8. 보호된 엔드포인트 접근
        response = requests.get(f'{AUTH_URL}/api/protected',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        assert response.json()['user'] == 'admin'

        # 9. 작업 삭제
        for task in tasks:
            response = requests.delete(f"{BASE_URL}/api/tasks/{task['id']}")
            assert response.status_code == 200

    def test_error_scenarios(self, setup_servers):
        """에러 시나리오 테스트"""

        # 잘못된 엔드포인트
        response = requests.get(f'{BASE_URL}/api/nonexistent')
        assert response.status_code == 404

        # 잘못된 인증 정보
        response = requests.post(f'{AUTH_URL}/api/login', json={
            'username': 'hacker',
            'password': 'wrong'
        })
        assert response.status_code == 401

        # 토큰 없이 보호된 리소스 접근
        response = requests.get(f'{AUTH_URL}/api/protected')
        assert response.status_code == 401

    def test_api_rate_limiting(self, setup_servers):
        """Rate Limiting 테스트 (구현 후)"""
        # 많은 요청 보내기
        responses = []
        for _ in range(100):
            response = requests.get(f'{BASE_URL}/api/tasks')
            responses.append(response.status_code)

        # 대부분 성공해야 함 (rate limiting이 있다면 일부 429)
        success_count = sum(1 for code in responses if code == 200)
        assert success_count > 90  # 90% 이상 성공

    def test_data_persistence(self, setup_servers):
        """데이터 지속성 테스트"""

        # 1. 작업 생성
        response = requests.post(f'{BASE_URL}/api/tasks', json={
            'title': 'Persistence Test',
            'description': 'This should persist'
        })
        assert response.status_code == 201
        task_id = response.json()['id']

        # 2. 작업 조회 (데이터가 유지되는지 확인)
        response = requests.get(f'{BASE_URL}/api/tasks/{task_id}')
        assert response.status_code == 200
        assert response.json()['title'] == 'Persistence Test'

        # 3. 정리
        requests.delete(f'{BASE_URL}/api/tasks/{task_id}')

    def test_concurrent_requests(self, setup_servers):
        """동시 요청 처리 테스트"""
        import concurrent.futures

        def make_request(i):
            return requests.get(f'{BASE_URL}/api/health')

        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_request, i) for i in range(100)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # 모든 요청이 성공해야 함
        success_count = sum(1 for r in responses if r.status_code == 200)
        assert success_count == 100

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
