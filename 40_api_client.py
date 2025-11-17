"""
40. API Client - REST API 클라이언트 라이브러리
"""
import requests
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import time

class APIClient:
    """범용 REST API 클라이언트"""

    def __init__(self, base_url, headers=None, timeout=30):
        """
        API 클라이언트 초기화

        Args:
            base_url: API 베이스 URL
            headers: 기본 헤더
            timeout: 타임아웃 (초)
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get(self, endpoint, params=None, **kwargs):
        """GET 요청"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json_data=None, **kwargs):
        """POST 요청"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def put(self, endpoint, data=None, json_data=None, **kwargs):
        """PUT 요청"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.put(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def patch(self, endpoint, data=None, json_data=None, **kwargs):
        """PATCH 요청"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.patch(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout,
            **kwargs
        )
        return self._handle_response(response)

    def delete(self, endpoint, **kwargs):
        """DELETE 요청"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.delete(url, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    def set_auth_token(self, token, token_type='Bearer'):
        """인증 토큰 설정"""
        self.session.headers['Authorization'] = f'{token_type} {token}'

    def set_header(self, key, value):
        """헤더 설정"""
        self.session.headers[key] = value

    def _handle_response(self, response):
        """응답 처리"""
        try:
            response.raise_for_status()

            # JSON 응답
            if 'application/json' in response.headers.get('Content-Type', ''):
                return response.json()

            # 텍스트 응답
            return response.text

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            raise

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise

class CachedAPIClient(APIClient):
    """캐싱 기능이 있는 API 클라이언트"""

    def __init__(self, base_url, cache_ttl=300, **kwargs):
        super().__init__(base_url, **kwargs)
        self.cache = {}
        self.cache_ttl = cache_ttl

    def get(self, endpoint, params=None, use_cache=True, **kwargs):
        """캐시를 사용하는 GET 요청"""
        cache_key = f"{endpoint}:{str(params)}"

        if use_cache and cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=self.cache_ttl):
                print(f"[CACHE HIT] {endpoint}")
                return cached_data

        # 캐시 미스 - API 호출
        print(f"[CACHE MISS] {endpoint}")
        data = super().get(endpoint, params, **kwargs)

        if use_cache:
            self.cache[cache_key] = (data, datetime.now())

        return data

    def clear_cache(self):
        """캐시 초기화"""
        self.cache = {}

class RateLimitedAPIClient(APIClient):
    """속도 제한이 있는 API 클라이언트"""

    def __init__(self, base_url, rate_limit=10, per_seconds=60, **kwargs):
        """
        Args:
            rate_limit: 요청 수 제한
            per_seconds: 제한 시간 (초)
        """
        super().__init__(base_url, **kwargs)
        self.rate_limit = rate_limit
        self.per_seconds = per_seconds
        self.request_times = []

    def _check_rate_limit(self):
        """속도 제한 확인"""
        now = time.time()

        # 오래된 요청 제거
        self.request_times = [t for t in self.request_times if now - t < self.per_seconds]

        # 제한 확인
        if len(self.request_times) >= self.rate_limit:
            sleep_time = self.per_seconds - (now - self.request_times[0])
            if sleep_time > 0:
                print(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                self.request_times = []

        self.request_times.append(now)

    def get(self, endpoint, **kwargs):
        """속도 제한을 적용한 GET 요청"""
        self._check_rate_limit()
        return super().get(endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        """속도 제한을 적용한 POST 요청"""
        self._check_rate_limit()
        return super().post(endpoint, **kwargs)

# 실제 API 예제
class GitHubClient(APIClient):
    """GitHub API 클라이언트"""

    def __init__(self, token=None):
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if token:
            headers['Authorization'] = f'token {token}'

        super().__init__('https://api.github.com', headers=headers)

    def get_user(self, username):
        """사용자 정보 조회"""
        return self.get(f'/users/{username}')

    def get_repos(self, username):
        """사용자 저장소 목록"""
        return self.get(f'/users/{username}/repos')

    def get_repo(self, owner, repo):
        """저장소 정보"""
        return self.get(f'/repos/{owner}/{repo}')

# 사용 예제
if __name__ == '__main__':
    print("=== API Client Demo ===\n")

    # 1. 기본 API 클라이언트
    print("1. Basic API Client (JSONPlaceholder)")
    client = APIClient('https://jsonplaceholder.typicode.com')

    # GET 요청
    posts = client.get('/posts', params={'userId': 1})
    print(f"Found {len(posts)} posts")
    if posts:
        print(f"First post: {posts[0]['title']}")

    # POST 요청
    new_post = client.post('/posts', json_data={
        'title': 'New Post',
        'body': 'This is a new post',
        'userId': 1
    })
    print(f"\nCreated post: {new_post.get('id')}")

    # 2. 캐시 API 클라이언트
    print("\n2. Cached API Client")
    cached_client = CachedAPIClient('https://jsonplaceholder.typicode.com', cache_ttl=60)

    # 첫 번째 요청 (캐시 미스)
    data1 = cached_client.get('/users/1')
    print(f"User: {data1.get('name')}")

    # 두 번째 요청 (캐시 히트)
    data2 = cached_client.get('/users/1')
    print(f"User: {data2.get('name')}")

    # 3. 속도 제한 API 클라이언트
    print("\n3. Rate Limited API Client")
    limited_client = RateLimitedAPIClient(
        'https://jsonplaceholder.typicode.com',
        rate_limit=3,
        per_seconds=5
    )

    # 여러 요청 (속도 제한 적용)
    for i in range(1, 5):
        user = limited_client.get(f'/users/{i}')
        print(f"Request {i}: {user.get('name')}")

    # 4. GitHub API 클라이언트
    print("\n4. GitHub API Client")
    github = GitHubClient()

    try:
        user = github.get_user('torvalds')
        print(f"GitHub User: {user.get('name')}")
        print(f"Public Repos: {user.get('public_repos')}")
    except Exception as e:
        print(f"GitHub API error: {e}")

    print("\nNote: Install requests with: pip install requests")
