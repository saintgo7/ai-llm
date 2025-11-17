"""
Integration Tests - 여러 컴포넌트 간의 통합 테스트
"""
import sys
import os
import pytest
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Flask test client imports
from flask import Flask
from flask.testing import FlaskClient

class TestAPIIntegration:
    """REST API와 JWT 인증의 통합 테스트"""

    @pytest.fixture
    def api_client(self):
        """REST API 테스트 클라이언트"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '01_web_api'))
        from importlib import import_module
        rest_api = import_module('01_rest_api_server')
        rest_api.app.config['TESTING'] = True
        return rest_api.app.test_client()

    @pytest.fixture
    def auth_client(self):
        """JWT 인증 테스트 클라이언트"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '01_web_api'))
        from importlib import import_module
        jwt_auth = import_module('04_jwt_authentication')
        jwt_auth.app.config['TESTING'] = True
        return jwt_auth.app.test_client()

    def test_full_task_workflow(self, api_client):
        """전체 작업 워크플로우 테스트: 생성 -> 조회 -> 수정 -> 삭제"""
        # 1. 작업 생성
        response = api_client.post('/api/tasks',
            json={'title': 'Integration Test Task', 'description': 'Test'},
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        task_id = data['id']
        assert data['title'] == 'Integration Test Task'

        # 2. 작업 조회
        response = api_client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == task_id

        # 3. 작업 수정
        response = api_client.put(f'/api/tasks/{task_id}',
            json={'completed': True},
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['completed'] is True

        # 4. 작업 삭제
        response = api_client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200

        # 5. 삭제 확인
        response = api_client.get(f'/api/tasks/{task_id}')
        assert response.status_code == 404

    def test_authentication_workflow(self, auth_client):
        """인증 워크플로우 테스트: 로그인 -> 토큰 검증 -> 보호된 리소스 접근"""
        # 1. 로그인
        response = auth_client.post('/api/login',
            json={'username': 'admin', 'password': 'admin123'},
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        token = data['token']

        # 2. 토큰 검증
        response = auth_client.get('/api/verify',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['valid'] is True

        # 3. 보호된 리소스 접근
        response = auth_client.get('/api/protected',
            headers={'Authorization': f'Bearer {token}'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user'] == 'admin'

    def test_invalid_authentication(self, auth_client):
        """잘못된 인증 시도 테스트"""
        # 잘못된 비밀번호
        response = auth_client.post('/api/login',
            json={'username': 'admin', 'password': 'wrong'},
            content_type='application/json'
        )
        assert response.status_code == 401

        # 잘못된 토큰으로 접근
        response = auth_client.get('/api/protected',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        assert response.status_code == 401

    def test_api_error_handling(self, api_client):
        """API 에러 처리 통합 테스트"""
        # 잘못된 Content-Type
        response = api_client.post('/api/tasks',
            data='not json',
            content_type='text/plain'
        )
        assert response.status_code == 400

        # 필수 필드 누락
        response = api_client.post('/api/tasks',
            json={'description': 'No title'},
            content_type='application/json'
        )
        assert response.status_code == 400

        # 존재하지 않는 리소스
        response = api_client.get('/api/tasks/99999')
        assert response.status_code == 404

    def test_health_checks(self, api_client):
        """헬스 체크 테스트"""
        response = api_client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data

    def test_concurrent_task_creation(self, api_client):
        """동시 작업 생성 테스트"""
        import concurrent.futures

        def create_task(index):
            return api_client.post('/api/tasks',
                json={'title': f'Task {index}', 'description': f'Desc {index}'},
                content_type='application/json'
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_task, i) for i in range(10)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # 모든 요청이 성공해야 함
        for response in responses:
            assert response.status_code == 201

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
