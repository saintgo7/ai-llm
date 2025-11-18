# 🔢 자료구조 & 알고리즘

이 폴더에는 클래식 자료구조와 알고리즘의 완전한 구현 10개가 포함되어 있습니다.

> **📚 전체 사용 설명서**: 상세한 한글 가이드는 [사용설명서.md](./사용설명서.md)를 참조하세요.

## 📋 프로그램 목록

### 11. 이진 탐색 트리 (BST)
**파일**: `11_binary_search_tree.py`

모든 연산을 포함한 완전한 BST 구현입니다.

**주요 기능**:
- 삽입, 삭제, 검색
- 중위/전위/후위 순회
- 높이 및 크기 계산
- 균형 연산

**실행 방법**:
```bash
python 11_binary_search_tree.py
```

**사용 예시**:
```python
from binary_search_tree import BinarySearchTree

bst = BinarySearchTree()
bst.insert(50)
bst.insert(30)
bst.insert(70)
print(bst.search(30))  # True
print(bst.inorder())   # [30, 50, 70]
```

**시간 복잡도**:
- 삽입: O(log n) 평균, O(n) 최악
- 검색: O(log n) 평균, O(n) 최악
- 삭제: O(log n) 평균, O(n) 최악

---

### 12. 정렬 알고리즘
**파일**: `12_sorting_algorithms.py`

벤치마킹 기능이 포함된 7가지 정렬 알고리즘입니다.

**알고리즘**:
- 버블 정렬 O(n²)
- 선택 정렬 O(n²)
- 삽입 정렬 O(n²)
- 병합 정렬 O(n log n)
- 퀵 정렬 O(n log n)
- 힙 정렬 O(n log n)
- 계수 정렬 O(n + k)

**실행 방법**:
```bash
python 12_sorting_algorithms.py
```

**성능 비교**:
```python
import time
from sorting_algorithms import SortingAlgorithms

sa = SortingAlgorithms()
data = [64, 34, 25, 12, 22, 11, 90]

start = time.time()
sorted_data = sa.quick_sort(data.copy())
print(f"퀵 정렬 시간: {time.time() - start:.6f}초")
```

---

### 13. 그래프 알고리즘
**파일**: `13_graph_algorithms.py`

포괄적인 그래프 알고리즘 구현입니다.

**알고리즘**:
- BFS (너비 우선 탐색)
- DFS (깊이 우선 탐색)
- 다익스트라 최단 경로
- 벨만-포드 알고리즘
- 사이클 감지
- 위상 정렬
- 크루스칼 MST

**실행 방법**:
```bash
python 13_graph_algorithms.py
```

**실전 활용**:
```python
from graph_algorithms import Graph

# 도시 간 거리 네트워크
graph = Graph()
graph.add_edge("서울", "부산", 325)
graph.add_edge("서울", "대전", 140)
graph.add_edge("대전", "부산", 200)

# 최단 경로 찾기
shortest_path = graph.dijkstra("서울", "부산")
print(f"최단 거리: {shortest_path}")
```

---

### 14. 동적 프로그래밍
**파일**: `14_dynamic_programming.py`

클래식 DP 문제와 해결법입니다.

**문제**:
- 피보나치 수열
- 0/1 배낭 문제
- 최장 공통 부분 수열 (LCS)
- 편집 거리
- 동전 거스름돈
- 최장 증가 부분 수열 (LIS)
- 행렬 연쇄 곱셈
- 막대 자르기
- 단어 분할

**실행 방법**:
```bash
python 14_dynamic_programming.py
```

**배낭 문제 예시**:
```python
from dynamic_programming import DynamicProgramming

dp = DynamicProgramming()
values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50

max_value = dp.knapsack_01(values, weights, capacity)
print(f"최대 가치: {max_value}")  # 220
```

---

### 15. 연결 리스트
**파일**: `15_linked_list.py`

단일 및 이중 연결 리스트 구현입니다.

**주요 기능**:
- 추가, 삽입, 삭제
- 검색 및 순회
- 역순 변환
- 사이클 감지
- 중복 제거

**실행 방법**:
```bash
python 15_linked_list.py
```

**사용 예시**:
```python
from linked_list import LinkedList

ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.display()  # 1 -> 2 -> 3
ll.reverse()
ll.display()  # 3 -> 2 -> 1
```

---

### 16. 스택 & 큐
**파일**: `16_stack_queue.py`

모든 스택과 큐 변형 구현입니다.

**구현**:
- 스택 (LIFO)
- 큐 (FIFO)
- 원형 큐
- 우선순위 큐
- 덱 (양방향 큐)
- 응용 (괄호 검사 등)

**실행 방법**:
```bash
python 16_stack_queue.py
```

**괄호 검사 예시**:
```python
from stack_queue import Stack

def is_balanced(expression):
    stack = Stack()
    pairs = {'(': ')', '{': '}', '[': ']'}

    for char in expression:
        if char in pairs:
            stack.push(char)
        elif char in pairs.values():
            if stack.is_empty() or pairs[stack.pop()] != char:
                return False
    return stack.is_empty()

print(is_balanced("{[()]}"))  # True
print(is_balanced("{[(])}"))  # False
```

---

### 17. 해시 테이블
**파일**: `17_hash_table.py`

충돌 해결이 포함된 해시 테이블입니다.

**주요 기능**:
- 체이닝 방식
- 개방 주소법
- 동적 크기 조정
- 부하율 관리
- 응용 (Two Sum, 중복 검사 등)

**실행 방법**:
```bash
python 17_hash_table.py
```

**Two Sum 문제**:
```python
from hash_table import HashTable

def two_sum(nums, target):
    ht = HashTable()
    for i, num in enumerate(nums):
        complement = target - num
        if ht.get(complement) is not None:
            return [ht.get(complement), i]
        ht.insert(num, i)
    return None

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

---

### 18. 힙
**파일**: `18_heap.py`

최소/최대 힙 및 우선순위 큐입니다.

**주요 기능**:
- 최소 힙
- 최대 힙
- 우선순위 큐
- 힙 정렬
- K개의 최대 원소
- K개의 정렬된 리스트 병합

**실행 방법**:
```bash
python 18_heap.py
```

**K개의 최대 원소**:
```python
from heap import MaxHeap

def k_largest(nums, k):
    heap = MaxHeap()
    for num in nums:
        heap.insert(num)

    result = []
    for _ in range(k):
        result.append(heap.extract())
    return result

print(k_largest([3, 2, 1, 5, 6, 4], 2))  # [6, 5]
```

---

### 19. 트라이
**파일**: `19_trie.py`

접두사 트리 (Trie) 자료구조입니다.

**주요 기능**:
- 삽입, 검색, 삭제
- 접두사 검색
- 자동 완성
- 맞춤법 검사
- 단어 빈도

**실행 방법**:
```bash
python 19_trie.py
```

**자동 완성 예시**:
```python
from trie import Trie

trie = Trie()
words = ["apple", "app", "application", "apply"]
for word in words:
    trie.insert(word)

suggestions = trie.autocomplete("app")
print(suggestions)  # ['app', 'apple', 'application', 'apply']
```

---

### 20. 백트래킹
**파일**: `20_backtracking.py`

백트래킹 알고리즘 구현입니다.

**문제**:
- N-퀸 문제
- 스도쿠 솔버
- 순열
- 조합
- 부분집합의 합
- 단어 검색
- 괄호 생성
- 팰린드롬 분할
- 나이트 투어

**실행 방법**:
```bash
python 20_backtracking.py
```

**N-퀸 문제**:
```python
from backtracking import Backtracking

bt = Backtracking()
solutions = bt.solve_n_queens(4)
for solution in solutions:
    bt.print_board(solution)
```

---

## ⚡ 빠른 시작

### 1. 프로그램 실행
```bash
cd 02_data_structures_algorithms
python 11_binary_search_tree.py
```

### 2. 대화형 테스트
```python
# Python 인터프리터에서
from binary_search_tree import BinarySearchTree

bst = BinarySearchTree()
bst.insert(50)
bst.insert(30)
bst.insert(70)
print(bst.inorder())
```

## 📊 복잡도 분석

| 알고리즘 | 시간 복잡도 | 공간 복잡도 |
|----------|-------------|-------------|
| BST 검색 | O(log n) 평균, O(n) 최악 | O(1) |
| 병합 정렬 | O(n log n) | O(n) |
| 퀵 정렬 | O(n log n) 평균, O(n²) 최악 | O(log n) |
| 다익스트라 | O((V+E) log V) | O(V) |
| 해시 테이블 | O(1) 평균 | O(n) |
| 힙 연산 | O(log n) | O(1) |
| 트라이 검색 | O(m), m=키 길이 | O(ALPHABET_SIZE * N) |

## 🎯 학습 경로

### 초급 - 기본 자료구조
1. 스택 & 큐 (16)
2. 연결 리스트 (15)
3. 해시 테이블 (17)

### 중급 - 트리와 정렬
4. 이진 탐색 트리 (11)
5. 힙 (18)
6. 정렬 알고리즘 (12)
7. 트라이 (19)

### 고급 - 알고리즘 기법
8. 그래프 알고리즘 (13)
9. 동적 프로그래밍 (14)
10. 백트래킹 (20)

## 🔧 문제 해결

### 재귀 깊이 초과 에러
```python
import sys
sys.setrecursionlimit(10000)  # 재귀 한도 증가
```

### 메모리 부족 (대용량 데이터)
```python
# 제너레이터 사용
def large_data_generator(n):
    for i in range(n):
        yield i

# 대신 리스트 전체를 메모리에 로드하지 않음
```

### 성능 측정
```python
import time
import tracemalloc

# 시간 측정
start = time.time()
your_function()
print(f"실행 시간: {time.time() - start:.6f}초")

# 메모리 측정
tracemalloc.start()
your_function()
current, peak = tracemalloc.get_traced_memory()
print(f"현재 메모리: {current / 10**6:.2f}MB")
print(f"피크 메모리: {peak / 10**6:.2f}MB")
tracemalloc.stop()
```

## 📚 실전 활용 예시

### 1. 네비게이션 시스템 (그래프)
```python
from graph_algorithms import Graph

# 도로 네트워크
road_network = Graph()
road_network.add_edge("A", "B", 5)
road_network.add_edge("B", "C", 3)

# 최단 경로
path = road_network.dijkstra("A", "C")
```

### 2. 작업 스케줄러 (힙)
```python
from heap import MinHeap

# 우선순위 기반 작업 스케줄링
task_queue = MinHeap()
task_queue.insert((1, "긴급 작업"))
task_queue.insert((5, "일반 작업"))

# 가장 우선순위 높은 작업 실행
priority, task = task_queue.extract()
```

### 3. LRU 캐시 (해시 + 연결 리스트)
```python
from collections import OrderedDict

class LRUCache:
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
```

## 🌟 코딩 테스트 대비

### 자주 나오는 문제 유형

**배열/문자열** (해시 테이블 활용):
- Two Sum, Three Sum
- Anagram 검사
- 중복 찾기

**트리** (BST, 힙):
- 트리 순회
- 최소 공통 조상 (LCA)
- 균형 트리 검증

**그래프**:
- 섬의 개수 (DFS/BFS)
- 최단 경로
- 사이클 감지

**동적 프로그래밍**:
- 0/1 배낭
- 계단 오르기
- 최장 증가 수열

## 📖 상세 가이드

각 프로그램의 상세한 설명, 실전 활용법, 최적화 기법은 **[사용설명서.md](./사용설명서.md)**를 참조하세요.

사용설명서에는 다음 내용이 포함되어 있습니다:
- 🎯 알고리즘 원리와 동작 과정
- 💡 실전 문제 해결 예시
- 🏆 최적화 기법과 모범 사례
- 🔍 시간/공간 복잡도 분석
- 🚀 코딩 테스트 대비 팁

---

**총 프로그램 수**: 10개 | **카테고리**: 자료구조 & 알고리즘

**도움이 필요하신가요?** [사용설명서.md](./사용설명서.md)를 확인하거나 이슈를 등록해 주세요!
