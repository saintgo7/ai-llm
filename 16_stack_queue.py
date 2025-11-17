"""
16. Stack & Queue - 스택과 큐 구현
"""

class Stack:
    """스택 (LIFO - Last In First Out)"""

    def __init__(self):
        self.items = []

    def is_empty(self):
        """스택이 비어있는지 확인"""
        return len(self.items) == 0

    def push(self, item):
        """항목 추가"""
        self.items.append(item)

    def pop(self):
        """항목 제거 및 반환"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items.pop()

    def peek(self):
        """맨 위 항목 확인"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self.items[-1]

    def size(self):
        """스택 크기"""
        return len(self.items)

    def __str__(self):
        return f"Stack({self.items})"

class Queue:
    """큐 (FIFO - First In First Out)"""

    def __init__(self):
        self.items = []

    def is_empty(self):
        """큐가 비어있는지 확인"""
        return len(self.items) == 0

    def enqueue(self, item):
        """항목 추가"""
        self.items.append(item)

    def dequeue(self):
        """항목 제거 및 반환"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items.pop(0)

    def front(self):
        """맨 앞 항목 확인"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.items[0]

    def size(self):
        """큐 크기"""
        return len(self.items)

    def __str__(self):
        return f"Queue({self.items})"

class CircularQueue:
    """원형 큐"""

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = [None] * capacity
        self.front = -1
        self.rear = -1
        self.count = 0

    def is_empty(self):
        """큐가 비어있는지 확인"""
        return self.count == 0

    def is_full(self):
        """큐가 가득 찼는지 확인"""
        return self.count == self.capacity

    def enqueue(self, item):
        """항목 추가"""
        if self.is_full():
            raise OverflowError("Queue is full")

        if self.front == -1:
            self.front = 0

        self.rear = (self.rear + 1) % self.capacity
        self.items[self.rear] = item
        self.count += 1

    def dequeue(self):
        """항목 제거 및 반환"""
        if self.is_empty():
            raise IndexError("Queue is empty")

        item = self.items[self.front]
        self.items[self.front] = None

        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = (self.front + 1) % self.capacity

        self.count -= 1
        return item

    def size(self):
        """큐 크기"""
        return self.count

    def __str__(self):
        if self.is_empty():
            return "CircularQueue([])"

        result = []
        i = self.front
        for _ in range(self.count):
            result.append(self.items[i])
            i = (i + 1) % self.capacity

        return f"CircularQueue({result})"

class PriorityQueue:
    """우선순위 큐 (최소 힙)"""

    def __init__(self):
        self.items = []

    def is_empty(self):
        """큐가 비어있는지 확인"""
        return len(self.items) == 0

    def enqueue(self, item, priority):
        """항목 추가 (우선순위 포함)"""
        self.items.append((priority, item))
        self.items.sort(key=lambda x: x[0])

    def dequeue(self):
        """가장 높은 우선순위 항목 제거 및 반환"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self.items.pop(0)[1]

    def peek(self):
        """가장 높은 우선순위 항목 확인"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self.items[0][1]

    def size(self):
        """큐 크기"""
        return len(self.items)

    def __str__(self):
        return f"PriorityQueue({[(p, i) for p, i in self.items]})"

class Deque:
    """덱 (양방향 큐)"""

    def __init__(self):
        self.items = []

    def is_empty(self):
        """덱이 비어있는지 확인"""
        return len(self.items) == 0

    def add_front(self, item):
        """앞에 항목 추가"""
        self.items.insert(0, item)

    def add_rear(self, item):
        """뒤에 항목 추가"""
        self.items.append(item)

    def remove_front(self):
        """앞에서 항목 제거"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items.pop(0)

    def remove_rear(self):
        """뒤에서 항목 제거"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items.pop()

    def peek_front(self):
        """앞 항목 확인"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items[0]

    def peek_rear(self):
        """뒤 항목 확인"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self.items[-1]

    def size(self):
        """덱 크기"""
        return len(self.items)

    def __str__(self):
        return f"Deque({self.items})"

# 실전 응용 예제
def balanced_parentheses(expression):
    """괄호 균형 검사 (스택 사용)"""
    stack = Stack()
    opening = "([{"
    closing = ")]}"
    pairs = {"(": ")", "[": "]", "{": "}"}

    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty():
                return False
            if pairs[stack.pop()] != char:
                return False

    return stack.is_empty()

def reverse_string(s):
    """문자열 뒤집기 (스택 사용)"""
    stack = Stack()
    for char in s:
        stack.push(char)

    result = ""
    while not stack.is_empty():
        result += stack.pop()

    return result

def hot_potato(names, num):
    """뜨거운 감자 게임 (큐 사용)"""
    queue = Queue()
    for name in names:
        queue.enqueue(name)

    while queue.size() > 1:
        for _ in range(num):
            queue.enqueue(queue.dequeue())
        queue.dequeue()

    return queue.dequeue()

if __name__ == '__main__':
    print("=== Stack Demo ===")
    stack = Stack()
    for i in [1, 2, 3, 4, 5]:
        stack.push(i)
    print(f"Stack: {stack}")
    print(f"Pop: {stack.pop()}")
    print(f"Peek: {stack.peek()}")
    print(f"Size: {stack.size()}")

    print("\n=== Queue Demo ===")
    queue = Queue()
    for i in [1, 2, 3, 4, 5]:
        queue.enqueue(i)
    print(f"Queue: {queue}")
    print(f"Dequeue: {queue.dequeue()}")
    print(f"Front: {queue.front()}")

    print("\n=== Circular Queue Demo ===")
    cq = CircularQueue(5)
    for i in range(1, 6):
        cq.enqueue(i)
    print(f"Circular Queue: {cq}")
    cq.dequeue()
    cq.dequeue()
    cq.enqueue(6)
    cq.enqueue(7)
    print(f"After operations: {cq}")

    print("\n=== Priority Queue Demo ===")
    pq = PriorityQueue()
    pq.enqueue("Task 1", 3)
    pq.enqueue("Task 2", 1)
    pq.enqueue("Task 3", 2)
    print(f"Priority Queue: {pq}")
    print(f"Highest priority: {pq.dequeue()}")

    print("\n=== Deque Demo ===")
    dq = Deque()
    dq.add_rear(1)
    dq.add_rear(2)
    dq.add_front(0)
    print(f"Deque: {dq}")

    print("\n=== Applications ===")
    expr = "{[()()]}"
    print(f"Balanced '{expr}': {balanced_parentheses(expr)}")
    print(f"Reversed 'Hello': {reverse_string('Hello')}")
    print(f"Hot Potato winner: {hot_potato(['A', 'B', 'C', 'D', 'E'], 7)}")
