"""
Unit Tests for REST API Server
"""
import sys
import os
import pytest
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import after path setup
from unittest.mock import MagicMock

class TestRestAPI:
    """REST API 테스트"""

    def test_validate_task_data_valid(self):
        """유효한 작업 데이터 테스트"""
        # Lazy import to avoid Flask initialization issues
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '01_web_api'))
        from importlib import import_module
        rest_api = import_module('01_rest_api_server')

        data = {
            'title': 'Test Task',
            'description': 'Test Description'
        }

        is_valid, error = rest_api.validate_task_data(data)
        assert is_valid is True
        assert error is None

    def test_validate_task_data_missing_title(self):
        """제목 누락 테스트"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '01_web_api'))
        from importlib import import_module
        rest_api = import_module('01_rest_api_server')

        data = {
            'description': 'Test Description'
        }

        is_valid, error = rest_api.validate_task_data(data)
        assert is_valid is False
        assert 'Title is required' in error

    def test_validate_task_data_title_too_long(self):
        """제목 길이 초과 테스트"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '01_web_api'))
        from importlib import import_module
        rest_api = import_module('01_rest_api_server')

        data = {
            'title': 'A' * 201,
            'description': 'Test'
        }

        is_valid, error = rest_api.validate_task_data(data)
        assert is_valid is False
        assert 'less than 200' in error

    def test_hash_password(self):
        """비밀번호 해싱 테스트"""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '01_web_api'))
        from importlib import import_module
        jwt_auth = import_module('04_jwt_authentication')

        password = 'testpassword123'
        hashed = jwt_auth.hash_password(password)

        # 해시는 64자 16진수 문자열이어야 함 (SHA256)
        assert len(hashed) == 64
        assert all(c in '0123456789abcdef' for c in hashed)

        # 같은 비밀번호는 같은 해시 생성
        assert jwt_auth.hash_password(password) == hashed

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
