"""
12. Sorting Algorithms - 다양한 정렬 알고리즘 구현
"""
import time
import random

class SortingAlgorithms:
    @staticmethod
    def bubble_sort(arr):
        """버블 정렬 - O(n²)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr

    @staticmethod
    def selection_sort(arr):
        """선택 정렬 - O(n²)"""
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    @staticmethod
    def insertion_sort(arr):
        """삽입 정렬 - O(n²)"""
        arr = arr.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    @staticmethod
    def merge_sort(arr):
        """병합 정렬 - O(n log n)"""
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left = SortingAlgorithms.merge_sort(arr[:mid])
        right = SortingAlgorithms.merge_sort(arr[mid:])

        return SortingAlgorithms._merge(left, right)

    @staticmethod
    def _merge(left, right):
        """병합 헬퍼 함수"""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    @staticmethod
    def quick_sort(arr):
        """퀵 정렬 - O(n log n) 평균"""
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return SortingAlgorithms.quick_sort(left) + middle + SortingAlgorithms.quick_sort(right)

    @staticmethod
    def heap_sort(arr):
        """힙 정렬 - O(n log n)"""
        arr = arr.copy()

        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        n = len(arr)

        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, n, i)

        # Extract elements from heap
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            heapify(arr, i, 0)

        return arr

    @staticmethod
    def counting_sort(arr):
        """계수 정렬 - O(n + k), 정수 배열에 적합"""
        if not arr:
            return arr

        min_val = min(arr)
        max_val = max(arr)
        range_size = max_val - min_val + 1

        count = [0] * range_size
        output = [0] * len(arr)

        for num in arr:
            count[num - min_val] += 1

        for i in range(1, len(count)):
            count[i] += count[i - 1]

        for num in reversed(arr):
            output[count[num - min_val] - 1] = num
            count[num - min_val] -= 1

        return output

    @staticmethod
    def benchmark(arr, algorithm_name):
        """정렬 알고리즘 벤치마크"""
        start_time = time.time()

        if algorithm_name == 'bubble':
            result = SortingAlgorithms.bubble_sort(arr)
        elif algorithm_name == 'selection':
            result = SortingAlgorithms.selection_sort(arr)
        elif algorithm_name == 'insertion':
            result = SortingAlgorithms.insertion_sort(arr)
        elif algorithm_name == 'merge':
            result = SortingAlgorithms.merge_sort(arr)
        elif algorithm_name == 'quick':
            result = SortingAlgorithms.quick_sort(arr)
        elif algorithm_name == 'heap':
            result = SortingAlgorithms.heap_sort(arr)
        elif algorithm_name == 'counting':
            result = SortingAlgorithms.counting_sort(arr)
        else:
            return None, 0

        end_time = time.time()
        return result, end_time - start_time

if __name__ == '__main__':
    # 테스트 데이터
    test_arr = [64, 34, 25, 12, 22, 11, 90, 88, 45, 50, 31, 17, 28, 19]

    print("Sorting Algorithms Demo")
    print(f"Original array: {test_arr}\n")

    algorithms = ['bubble', 'selection', 'insertion', 'merge', 'quick', 'heap', 'counting']

    for algo in algorithms:
        sorted_arr, exec_time = SortingAlgorithms.benchmark(test_arr, algo)
        print(f"{algo.capitalize()} Sort:")
        print(f"  Result: {sorted_arr}")
        print(f"  Time: {exec_time:.6f} seconds\n")

    # 성능 비교 (큰 배열)
    print("\n=== Performance Comparison (1000 random numbers) ===")
    large_arr = [random.randint(1, 1000) for _ in range(1000)]

    for algo in algorithms:
        _, exec_time = SortingAlgorithms.benchmark(large_arr, algo)
        print(f"{algo.capitalize():12} : {exec_time:.6f} seconds")
