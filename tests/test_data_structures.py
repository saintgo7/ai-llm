"""
Unit Tests for Data Structures
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '02_data_structures_algorithms'))

from importlib import import_module

class TestBinarySearchTree:
    """Binary Search Tree 테스트"""

    def test_insert_and_search(self):
        """삽입 및 검색 테스트"""
        bst_module = import_module('11_binary_search_tree')
        bst = bst_module.BinarySearchTree()

        values = [50, 30, 70, 20, 40, 60, 80]
        for value in values:
            bst.insert(value)

        # 모든 값이 검색 가능해야 함
        for value in values:
            assert bst.search(value) is True

        # 없는 값은 검색 불가
        assert bst.search(100) is False

    def test_inorder_traversal(self):
        """중위 순회 테스트 (정렬된 순서)"""
        bst_module = import_module('11_binary_search_tree')
        bst = bst_module.BinarySearchTree()

        values = [50, 30, 70, 20, 40, 60, 80]
        for value in values:
            bst.insert(value)

        result = bst.inorder_traversal()
        expected = sorted(values)

        assert result == expected

class TestSortingAlgorithms:
    """정렬 알고리즘 테스트"""

    def test_bubble_sort(self):
        """버블 정렬 테스트"""
        sort_module = import_module('12_sorting_algorithms')
        sorter = sort_module.SortingAlgorithms()

        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.bubble_sort(arr.copy())

        assert result == sorted(arr)

    def test_quick_sort(self):
        """퀵 정렬 테스트"""
        sort_module = import_module('12_sorting_algorithms')
        sorter = sort_module.SortingAlgorithms()

        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.quick_sort(arr.copy())

        assert result == sorted(arr)

class TestDynamicProgramming:
    """Dynamic Programming 테스트"""

    def test_fibonacci(self):
        """피보나치 수열 테스트"""
        dp_module = import_module('14_dynamic_programming')
        dp = dp_module.DynamicProgramming()

        assert dp.fibonacci(0) == 0
        assert dp.fibonacci(1) == 1
        assert dp.fibonacci(10) == 55

    def test_coin_change(self):
        """동전 거스름돈 테스트"""
        dp_module = import_module('14_dynamic_programming')
        dp = dp_module.DynamicProgramming()

        coins = [1, 2, 5]
        assert dp.coin_change(coins, 11) == 3  # 5+5+1
        assert dp.coin_change(coins, 3) == 2   # 2+1

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
