"""
28. Caching System - 캐싱 시스템 구현
"""
import time
import pickle
import hashlib
from functools import wraps
from collections import OrderedDict
from datetime import datetime, timedelta

class Cache:
    """간단한 메모리 캐시"""

    def __init__(self, max_size=100, ttl=None):
        """
        Args:
            max_size: 최대 캐시 크기
            ttl: Time To Live (초), None이면 무제한
        """
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.hit_count = 0
        self.miss_count = 0

    def get(self, key):
        """캐시에서 값 가져오기"""
        if key in self.cache:
            value, expiry = self.cache[key]

            # TTL 체크
            if expiry and datetime.now() > expiry:
                del self.cache[key]
                self.miss_count += 1
                return None

            # LRU: 최근 사용한 항목을 맨 뒤로
            self.cache.move_to_end(key)
            self.hit_count += 1
            return value

        self.miss_count += 1
        return None

    def set(self, key, value):
        """캐시에 값 저장"""
        # TTL 설정
        expiry = None
        if self.ttl:
            expiry = datetime.now() + timedelta(seconds=self.ttl)

        # 이미 존재하면 업데이트
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = (value, expiry)
        else:
            # 크기 초과시 가장 오래된 항목 제거
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)

            self.cache[key] = (value, expiry)

    def delete(self, key):
        """캐시에서 삭제"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self):
        """캐시 전체 삭제"""
        self.cache.clear()
        self.hit_count = 0
        self.miss_count = 0

    def get_stats(self):
        """캐시 통계"""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0

        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hit_count,
            'misses': self.miss_count,
            'hit_rate': hit_rate
        }

class LRUCache:
    """LRU (Least Recently Used) 캐시"""

    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

class FileCache:
    """파일 기반 캐시"""

    def __init__(self, cache_dir='.cache'):
        import os
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, key):
        """캐시 파일 경로 생성"""
        key_hash = hashlib.md5(str(key).encode()).hexdigest()
        return f"{self.cache_dir}/{key_hash}.cache"

    def get(self, key):
        """캐시 파일에서 읽기"""
        cache_path = self._get_cache_path(key)

        try:
            with open(cache_path, 'rb') as f:
                data = pickle.load(f)
                expiry = data.get('expiry')

                if expiry and datetime.now() > expiry:
                    self.delete(key)
                    return None

                return data['value']
        except (FileNotFoundError, EOFError):
            return None

    def set(self, key, value, ttl=None):
        """캐시 파일에 저장"""
        cache_path = self._get_cache_path(key)
        expiry = None

        if ttl:
            expiry = datetime.now() + timedelta(seconds=ttl)

        data = {
            'value': value,
            'expiry': expiry,
            'created': datetime.now()
        }

        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)

    def delete(self, key):
        """캐시 파일 삭제"""
        import os
        cache_path = self._get_cache_path(key)
        try:
            os.remove(cache_path)
            return True
        except FileNotFoundError:
            return False

def memoize(ttl=None):
    """함수 결과 캐싱 데코레이터"""
    cache = Cache(ttl=ttl)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 캐시 키 생성
            key = str(args) + str(sorted(kwargs.items()))

            # 캐시 확인
            result = cache.get(key)
            if result is not None:
                print(f"[CACHE HIT] {func.__name__}{args}")
                return result

            # 함수 실행 및 캐싱
            print(f"[CACHE MISS] {func.__name__}{args}")
            result = func(*args, **kwargs)
            cache.set(key, result)

            return result

        wrapper.cache = cache
        wrapper.cache_clear = cache.clear
        wrapper.cache_stats = cache.get_stats

        return wrapper

    return decorator

# 사용 예제
@memoize(ttl=10)
def expensive_function(n):
    """시간이 오래 걸리는 함수 시뮬레이션"""
    print(f"  Computing result for {n}...")
    time.sleep(1)  # 1초 대기
    return n * n

@memoize()
def fibonacci(n):
    """피보나치 (캐싱 없이는 매우 느림)"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == '__main__':
    print("=== Basic Cache Demo ===")
    cache = Cache(max_size=3)

    cache.set('key1', 'value1')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')

    print(f"Get key1: {cache.get('key1')}")
    print(f"Get key2: {cache.get('key2')}")
    print(f"Get invalid: {cache.get('invalid')}")

    cache.set('key4', 'value4')  # key3이 제거됨 (LRU)
    print(f"Get key3 (should be None): {cache.get('key3')}")

    print(f"\nCache stats: {cache.get_stats()}")

    print("\n=== Memoization Demo ===")
    print("First call (should compute):")
    result1 = expensive_function(5)
    print(f"Result: {result1}")

    print("\nSecond call (should use cache):")
    result2 = expensive_function(5)
    print(f"Result: {result2}")

    print(f"\nCache stats: {expensive_function.cache_stats()}")

    print("\n=== Fibonacci with Memoization ===")
    start = time.time()
    result = fibonacci(30)
    end = time.time()
    print(f"fibonacci(30) = {result}")
    print(f"Time: {end - start:.4f} seconds")

    print("\n=== File Cache Demo ===")
    file_cache = FileCache()
    file_cache.set('user_data', {'name': 'Alice', 'age': 30})
    print(f"Retrieved: {file_cache.get('user_data')}")
