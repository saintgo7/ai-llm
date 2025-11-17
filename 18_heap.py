"""
18. Heap - 힙 (우선순위 큐) 구현
"""

class MinHeap:
    """최소 힙"""

    def __init__(self):
        self.heap = []

    def parent(self, i):
        """부모 노드 인덱스"""
        return (i - 1) // 2

    def left_child(self, i):
        """왼쪽 자식 노드 인덱스"""
        return 2 * i + 1

    def right_child(self, i):
        """오른쪽 자식 노드 인덱스"""
        return 2 * i + 2

    def swap(self, i, j):
        """두 노드 교환"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, value):
        """값 삽입"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """위로 힙 속성 유지"""
        parent = self.parent(i)

        if i > 0 and self.heap[i] < self.heap[parent]:
            self.swap(i, parent)
            self._heapify_up(parent)

    def extract_min(self):
        """최소값 추출"""
        if not self.heap:
            raise IndexError("Heap is empty")

        if len(self.heap) == 1:
            return self.heap.pop()

        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return min_val

    def _heapify_down(self, i):
        """아래로 힙 속성 유지"""
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left

        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right

        if min_index != i:
            self.swap(i, min_index)
            self._heapify_down(min_index)

    def peek(self):
        """최소값 확인 (제거하지 않음)"""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def size(self):
        """힙 크기"""
        return len(self.heap)

    def is_empty(self):
        """힙이 비어있는지 확인"""
        return len(self.heap) == 0

    def __str__(self):
        return f"MinHeap({self.heap})"

class MaxHeap:
    """최대 힙"""

    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, value):
        """값 삽입"""
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """위로 힙 속성 유지"""
        parent = self.parent(i)

        if i > 0 and self.heap[i] > self.heap[parent]:
            self.swap(i, parent)
            self._heapify_up(parent)

    def extract_max(self):
        """최대값 추출"""
        if not self.heap:
            raise IndexError("Heap is empty")

        if len(self.heap) == 1:
            return self.heap.pop()

        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return max_val

    def _heapify_down(self, i):
        """아래로 힙 속성 유지"""
        max_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < len(self.heap) and self.heap[left] > self.heap[max_index]:
            max_index = left

        if right < len(self.heap) and self.heap[right] > self.heap[max_index]:
            max_index = right

        if max_index != i:
            self.swap(i, max_index)
            self._heapify_down(max_index)

    def peek(self):
        """최대값 확인"""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def __str__(self):
        return f"MaxHeap({self.heap})"

class PriorityQueue:
    """우선순위 큐 (MinHeap 기반)"""

    def __init__(self):
        self.heap = []

    def push(self, item, priority):
        """항목 추가"""
        self.heap.append((priority, item))
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        """최우선 항목 제거"""
        if not self.heap:
            raise IndexError("Priority queue is empty")

        if len(self.heap) == 1:
            return self.heap.pop()[1]

        priority, item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)

        return item

    def peek(self):
        """최우선 항목 확인"""
        if not self.heap:
            raise IndexError("Priority queue is empty")
        return self.heap[0][1]

    def _heapify_up(self, i):
        parent = (i - 1) // 2
        if i > 0 and self.heap[i][0] < self.heap[parent][0]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._heapify_up(parent)

    def _heapify_down(self, i):
        min_index = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < len(self.heap) and self.heap[left][0] < self.heap[min_index][0]:
            min_index = left

        if right < len(self.heap) and self.heap[right][0] < self.heap[min_index][0]:
            min_index = right

        if min_index != i:
            self.heap[i], self.heap[min_index] = self.heap[min_index], self.heap[i]
            self._heapify_down(min_index)

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

# 힙 응용 예제
def find_k_largest(arr, k):
    """배열에서 k번째로 큰 원소들 찾기"""
    min_heap = MinHeap()

    for num in arr:
        if min_heap.size() < k:
            min_heap.insert(num)
        elif num > min_heap.peek():
            min_heap.extract_min()
            min_heap.insert(num)

    return sorted([min_heap.extract_min() for _ in range(min_heap.size())], reverse=True)

def merge_k_sorted_lists(lists):
    """k개의 정렬된 리스트 병합"""
    pq = PriorityQueue()
    result = []

    # 각 리스트의 첫 원소를 우선순위 큐에 추가
    for i, lst in enumerate(lists):
        if lst:
            pq.push((i, 0, lst[0]), lst[0])  # (리스트 인덱스, 원소 인덱스, 값)

    while not pq.is_empty():
        list_idx, elem_idx, value = pq.pop()
        result.append(value)

        # 해당 리스트의 다음 원소 추가
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            pq.push((list_idx, elem_idx + 1, next_val), next_val)

    return result

def heap_sort(arr):
    """힙 정렬"""
    max_heap = MaxHeap()

    # 모든 원소를 힙에 삽입
    for num in arr:
        max_heap.insert(num)

    # 힙에서 순서대로 추출
    sorted_arr = []
    while not max_heap.is_empty():
        sorted_arr.insert(0, max_heap.extract_max())

    return sorted_arr

if __name__ == '__main__':
    print("=== Min Heap Demo ===")
    min_heap = MinHeap()
    values = [5, 3, 8, 1, 9, 2, 7]

    for val in values:
        min_heap.insert(val)

    print(f"Min Heap after insertions: {min_heap}")
    print(f"Extract min: {min_heap.extract_min()}")
    print(f"After extraction: {min_heap}")
    print(f"Peek: {min_heap.peek()}")

    print("\n=== Max Heap Demo ===")
    max_heap = MaxHeap()

    for val in values:
        max_heap.insert(val)

    print(f"Max Heap after insertions: {max_heap}")
    print(f"Extract max: {max_heap.extract_max()}")
    print(f"After extraction: {max_heap}")

    print("\n=== Priority Queue Demo ===")
    pq = PriorityQueue()
    pq.push("Low priority task", 5)
    pq.push("High priority task", 1)
    pq.push("Medium priority task", 3)

    print("Processing tasks by priority:")
    while not pq.is_empty():
        print(f"  - {pq.pop()}")

    print("\n=== Applications ===")

    # K개의 가장 큰 원소
    arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    k = 3
    print(f"Top {k} largest in {arr}: {find_k_largest(arr, k)}")

    # K개의 정렬된 리스트 병합
    lists = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"\nMerge sorted lists {lists}:")
    print(f"Result: {merge_k_sorted_lists(lists)}")

    # 힙 정렬
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nHeap sort {arr}:")
    print(f"Sorted: {heap_sort(arr)}")
