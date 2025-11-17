"""
Performance Tests - 성능 테스트
"""
import pytest
import time
import statistics
from memory_profiler import profile

class TestPerformance:
    """성능 테스트"""

    @pytest.fixture
    def bst_module(self):
        """BST 모듈 로드"""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02_data_structures_algorithms'))
        from importlib import import_module
        return import_module('11_binary_search_tree')

    @pytest.fixture
    def sort_module(self):
        """정렬 모듈 로드"""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02_data_structures_algorithms'))
        from importlib import import_module
        return import_module('12_sorting_algorithms')

    @pytest.fixture
    def dp_module(self):
        """DP 모듈 로드"""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02_data_structures_algorithms'))
        from importlib import import_module
        return import_module('14_dynamic_programming')

    def test_bst_insertion_performance(self, bst_module, benchmark):
        """BST 삽입 성능 테스트"""
        def insert_items():
            bst = bst_module.BinarySearchTree()
            for i in range(1000):
                bst.insert(i)
            return bst

        result = benchmark(insert_items)
        assert result.size() == 1000

    def test_bst_search_performance(self, bst_module, benchmark):
        """BST 검색 성능 테스트"""
        bst = bst_module.BinarySearchTree()
        for i in range(1000):
            bst.insert(i)

        def search_items():
            found = 0
            for i in range(0, 1000, 10):
                if bst.search(i):
                    found += 1
            return found

        result = benchmark(search_items)
        assert result == 100

    def test_sorting_performance(self, sort_module, benchmark):
        """정렬 알고리즘 성능 비교"""
        import random

        data = [random.randint(1, 10000) for _ in range(1000)]
        sorter = sort_module.SortingAlgorithms()

        # Quick Sort 성능
        result = benchmark(sorter.quick_sort, data.copy())
        assert result == sorted(data)

    def test_fibonacci_performance(self, dp_module):
        """피보나치 성능 테스트 (메모이제이션 vs 타뷸레이션)"""
        dp = dp_module.DynamicProgramming()

        # 메모이제이션
        start = time.time()
        result1 = dp.fibonacci(30)
        memo_time = time.time() - start

        # 타뷸레이션
        start = time.time()
        result2 = dp.fibonacci_tabulation(30)
        tabulation_time = time.time() - start

        assert result1 == result2
        print(f"\nMemoization: {memo_time:.6f}s")
        print(f"Tabulation: {tabulation_time:.6f}s")

    def test_api_response_time(self):
        """API 응답 시간 테스트"""
        import requests

        response_times = []
        for _ in range(100):
            start = time.time()
            response = requests.get('http://localhost:5000/api/health')
            elapsed = time.time() - start

            if response.status_code == 200:
                response_times.append(elapsed)

        if response_times:
            avg_time = statistics.mean(response_times)
            median_time = statistics.median(response_times)
            p95_time = sorted(response_times)[int(len(response_times) * 0.95)]

            print(f"\nAPI Response Times:")
            print(f"  Average: {avg_time*1000:.2f}ms")
            print(f"  Median: {median_time*1000:.2f}ms")
            print(f"  P95: {p95_time*1000:.2f}ms")

            # 응답 시간이 100ms 이하여야 함
            assert avg_time < 0.1, f"Average response time {avg_time}s exceeds 100ms"

    def test_memory_usage(self, bst_module):
        """메모리 사용량 테스트"""
        import tracemalloc

        tracemalloc.start()

        # BST에 대량 데이터 삽입
        bst = bst_module.BinarySearchTree()
        for i in range(10000):
            bst.insert(i)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"\nMemory Usage:")
        print(f"  Current: {current / 1024 / 1024:.2f} MB")
        print(f"  Peak: {peak / 1024 / 1024:.2f} MB")

        # 피크 메모리가 100MB를 넘지 않아야 함
        assert peak < 100 * 1024 * 1024

    def test_database_query_performance(self):
        """데이터베이스 쿼리 성능 테스트"""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '03_database_file_processing'))
        from importlib import import_module

        db_module = import_module('21_sqlite_database')

        with db_module.DatabaseManager(':memory:') as db:
            db.create_users_table()

            # 삽입 성능
            start = time.time()
            for i in range(1000):
                db.insert_user(f'user{i}', f'user{i}@example.com', f'pass{i}')
            insert_time = time.time() - start

            # 조회 성능
            start = time.time()
            users = db.get_all_users()
            query_time = time.time() - start

            print(f"\nDatabase Performance:")
            print(f"  Insert 1000 records: {insert_time:.3f}s")
            print(f"  Query all records: {query_time:.3f}s")

            assert len(users) == 1000
            assert insert_time < 1.0  # 1초 이내

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
