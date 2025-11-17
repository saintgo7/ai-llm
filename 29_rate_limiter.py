"""
29. Rate Limiter - 속도 제한기 구현
"""
import time
from collections import deque, defaultdict
from functools import wraps
from datetime import datetime, timedelta

class TokenBucket:
    """토큰 버킷 알고리즘"""

    def __init__(self, capacity, refill_rate):
        """
        Args:
            capacity: 버킷 용량
            refill_rate: 초당 토큰 리필 속도
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def _refill(self):
        """토큰 리필"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate

        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def consume(self, tokens=1):
        """토큰 소비"""
        self._refill()

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True

        return False

    def get_tokens(self):
        """현재 토큰 수"""
        self._refill()
        return self.tokens

class SlidingWindowLog:
    """슬라이딩 윈도우 로그 알고리즘"""

    def __init__(self, max_requests, window_seconds):
        """
        Args:
            max_requests: 윈도우 당 최대 요청 수
            window_seconds: 윈도우 크기 (초)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = deque()

    def allow_request(self):
        """요청 허용 여부"""
        now = time.time()
        window_start = now - self.window_seconds

        # 윈도우 밖의 요청 제거
        while self.requests and self.requests[0] < window_start:
            self.requests.popleft()

        # 요청 수 확인
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True

        return False

    def get_remaining_requests(self):
        """남은 요청 수"""
        now = time.time()
        window_start = now - self.window_seconds

        # 윈도우 내 요청 수 계산
        valid_requests = sum(1 for req in self.requests if req >= window_start)
        return max(0, self.max_requests - valid_requests)

class FixedWindow:
    """고정 윈도우 카운터"""

    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.window_start = time.time()
        self.request_count = 0

    def allow_request(self):
        """요청 허용 여부"""
        now = time.time()

        # 새 윈도우 시작
        if now - self.window_start >= self.window_seconds:
            self.window_start = now
            self.request_count = 0

        # 요청 수 확인
        if self.request_count < self.max_requests:
            self.request_count += 1
            return True

        return False

class LeakyBucket:
    """리키 버킷 알고리즘"""

    def __init__(self, capacity, leak_rate):
        """
        Args:
            capacity: 버킷 용량
            leak_rate: 초당 누수 속도
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.water_level = 0
        self.last_leak = time.time()

    def _leak(self):
        """누수 처리"""
        now = time.time()
        elapsed = now - self.last_leak
        leaked = elapsed * self.leak_rate

        self.water_level = max(0, self.water_level - leaked)
        self.last_leak = now

    def add_drop(self, drops=1):
        """물방울 추가"""
        self._leak()

        if self.water_level + drops <= self.capacity:
            self.water_level += drops
            return True

        return False

class RateLimiter:
    """다중 사용자 지원 속도 제한기"""

    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.limiters = defaultdict(lambda: SlidingWindowLog(max_requests, window_seconds))

    def allow_request(self, user_id):
        """특정 사용자의 요청 허용 여부"""
        return self.limiters[user_id].allow_request()

    def get_remaining(self, user_id):
        """남은 요청 수"""
        return self.limiters[user_id].get_remaining_requests()

def rate_limit(max_requests, window_seconds):
    """속도 제한 데코레이터"""
    limiter = SlidingWindowLog(max_requests, window_seconds)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if limiter.allow_request():
                return func(*args, **kwargs)
            else:
                raise Exception(f"Rate limit exceeded: {max_requests} requests per {window_seconds}s")

        wrapper.get_remaining = limiter.get_remaining_requests
        return wrapper

    return decorator

def api_rate_limit(max_requests_per_minute=60):
    """API 속도 제한 데코레이터"""
    limiters = defaultdict(lambda: SlidingWindowLog(max_requests_per_minute, 60))

    def decorator(func):
        @wraps(func)
        def wrapper(user_id, *args, **kwargs):
            limiter = limiters[user_id]

            if limiter.allow_request():
                remaining = limiter.get_remaining_requests()
                print(f"[OK] User {user_id}: {remaining} requests remaining")
                return func(user_id, *args, **kwargs)
            else:
                print(f"[BLOCKED] User {user_id}: Rate limit exceeded")
                raise Exception(f"Rate limit exceeded for user {user_id}")

        return wrapper

    return decorator

# 사용 예제
@rate_limit(max_requests=5, window_seconds=10)
def limited_function():
    """속도 제한이 있는 함수"""
    return "Success!"

@api_rate_limit(max_requests_per_minute=3)
def api_endpoint(user_id, data):
    """API 엔드포인트 시뮬레이션"""
    return f"Processed data for user {user_id}: {data}"

if __name__ == '__main__':
    print("=== Token Bucket Demo ===")
    bucket = TokenBucket(capacity=10, refill_rate=1)

    for i in range(15):
        if bucket.consume(1):
            print(f"Request {i+1}: Allowed (tokens: {bucket.get_tokens():.2f})")
        else:
            print(f"Request {i+1}: Blocked (tokens: {bucket.get_tokens():.2f})")
        time.sleep(0.5)

    print("\n=== Sliding Window Log Demo ===")
    limiter = SlidingWindowLog(max_requests=3, window_seconds=5)

    for i in range(6):
        if limiter.allow_request():
            print(f"Request {i+1}: Allowed (remaining: {limiter.get_remaining_requests()})")
        else:
            print(f"Request {i+1}: Blocked")
        time.sleep(1)

    print("\n=== Rate Limited Function Demo ===")
    for i in range(7):
        try:
            result = limited_function()
            print(f"Call {i+1}: {result} (remaining: {limited_function.get_remaining()})")
        except Exception as e:
            print(f"Call {i+1}: {e}")
        time.sleep(1)

    print("\n=== API Rate Limiter Demo ===")
    for i in range(5):
        try:
            api_endpoint("user123", f"data_{i}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.5)
