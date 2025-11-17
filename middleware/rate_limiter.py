"""
Rate Limiting Middleware
다양한 알고리즘을 사용한 Rate Limiting 구현
"""
import time
import redis
from functools import wraps
from flask import request, jsonify
from collections import defaultdict, deque

class RateLimiter:
    """Rate Limiter 기본 클래스"""

    def __init__(self, requests_per_minute=60, strategy='token_bucket'):
        self.requests_per_minute = requests_per_minute
        self.strategy = strategy

        if strategy == 'redis':
            self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        else:
            # 메모리 기반 저장소
            self.requests = defaultdict(deque)

    def is_allowed(self, key):
        """요청 허용 여부 확인"""
        if self.strategy == 'fixed_window':
            return self._fixed_window(key)
        elif self.strategy == 'sliding_window':
            return self._sliding_window(key)
        elif self.strategy == 'token_bucket':
            return self._token_bucket(key)
        elif self.strategy == 'redis':
            return self._redis_rate_limit(key)
        else:
            return True

    def _fixed_window(self, key):
        """고정 윈도우 알고리즘"""
        current_minute = int(time.time() / 60)
        window_key = f"{key}:{current_minute}"

        if window_key not in self.requests:
            self.requests[window_key] = 0

        if self.requests[window_key] < self.requests_per_minute:
            self.requests[window_key] += 1
            return True

        return False

    def _sliding_window(self, key):
        """슬라이딩 윈도우 알고리즘"""
        now = time.time()
        minute_ago = now - 60

        # 1분 이전 요청 제거
        while self.requests[key] and self.requests[key][0] < minute_ago:
            self.requests[key].popleft()

        if len(self.requests[key]) < self.requests_per_minute:
            self.requests[key].append(now)
            return True

        return False

    def _token_bucket(self, key):
        """토큰 버킷 알고리즘"""
        now = time.time()

        if key not in self.requests:
            self.requests[key] = {
                'tokens': self.requests_per_minute,
                'last_update': now
            }

        bucket = self.requests[key]
        time_passed = now - bucket['last_update']
        tokens_to_add = time_passed * (self.requests_per_minute / 60.0)

        bucket['tokens'] = min(
            self.requests_per_minute,
            bucket['tokens'] + tokens_to_add
        )
        bucket['last_update'] = now

        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            return True

        return False

    def _redis_rate_limit(self, key):
        """Redis 기반 Rate Limiting"""
        try:
            # Sliding window with Redis
            now = time.time()
            window_key = f"rate_limit:{key}"

            # Add current request
            self.redis_client.zadd(window_key, {now: now})

            # Remove requests older than 60 seconds
            self.redis_client.zremrangebyscore(window_key, 0, now - 60)

            # Count requests in window
            count = self.redis_client.zcard(window_key)

            # Set expiration
            self.redis_client.expire(window_key, 60)

            return count <= self.requests_per_minute
        except:
            # Fallback to allowing request if Redis fails
            return True

def rate_limit(requests_per_minute=60, strategy='token_bucket'):
    """Rate limiting 데코레이터"""
    limiter = RateLimiter(requests_per_minute, strategy)

    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get client identifier (IP address or user ID)
            if hasattr(request, 'user_id'):
                key = f"user:{request.user_id}"
            else:
                key = f"ip:{request.remote_addr}"

            if not limiter.is_allowed(key):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Maximum {requests_per_minute} requests per minute allowed',
                    'retry_after': 60
                }), 429

            return f(*args, **kwargs)
        return wrapped
    return decorator

# 글로벌 Rate Limiter
global_limiter = RateLimiter(requests_per_minute=100, strategy='sliding_window')

def setup_rate_limiting(app):
    """Flask 앱에 전역 Rate Limiting 적용"""

    @app.before_request
    def apply_rate_limiting():
        """모든 요청에 Rate Limiting 적용"""
        # Health check는 제외
        if request.endpoint == 'health_check':
            return

        key = f"ip:{request.remote_addr}"

        if not global_limiter.is_allowed(key):
            return jsonify({
                'error': 'Too many requests',
                'message': 'Global rate limit exceeded',
                'retry_after': 60
            }), 429

    return app

# 사용 예제:
# from middleware.rate_limiter import rate_limit, setup_rate_limiting
#
# app = Flask(__name__)
# setup_rate_limiting(app)
#
# @app.route('/api/resource')
# @rate_limit(requests_per_minute=30, strategy='token_bucket')
# def resource():
#     return jsonify({'data': 'resource'})
