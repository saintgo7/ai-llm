"""
15. Linked List - 연결 리스트 구현
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        """리스트가 비어있는지 확인"""
        return self.head is None

    def append(self, data):
        """끝에 노드 추가"""
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.size += 1

    def prepend(self, data):
        """앞에 노드 추가"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, index, data):
        """특정 위치에 노드 삽입"""
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")

        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def delete(self, data):
        """특정 값을 가진 첫 번째 노드 삭제"""
        if self.is_empty():
            return False

        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next

        return False

    def delete_at(self, index):
        """특정 위치의 노드 삭제"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        if index == 0:
            self.head = self.head.next
            self.size -= 1
            return

        current = self.head
        for _ in range(index - 1):
            current = current.next

        current.next = current.next.next
        self.size -= 1

    def search(self, data):
        """값 검색"""
        current = self.head
        index = 0

        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1

        return -1

    def get(self, index):
        """특정 위치의 값 반환"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")

        current = self.head
        for _ in range(index):
            current = current.next

        return current.data

    def reverse(self):
        """리스트 뒤집기"""
        prev = None
        current = self.head

        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        self.head = prev

    def get_middle(self):
        """중간 노드 찾기 (Fast & Slow pointer)"""
        if self.is_empty():
            return None

        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow.data

    def has_cycle(self):
        """사이클 존재 여부 확인 (Floyd's Cycle Detection)"""
        if self.is_empty():
            return False

        slow = fast = self.head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False

    def remove_duplicates(self):
        """중복 제거"""
        if self.is_empty():
            return

        seen = set()
        current = self.head
        seen.add(current.data)
        prev = current
        current = current.next

        while current:
            if current.data in seen:
                prev.next = current.next
                self.size -= 1
            else:
                seen.add(current.data)
                prev = current
            current = current.next

    def to_list(self):
        """리스트로 변환"""
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    def __str__(self):
        """문자열 표현"""
        return ' -> '.join(map(str, self.to_list())) + ' -> None'

    def __len__(self):
        """길이 반환"""
        return self.size

class DoublyNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        """끝에 노드 추가"""
        new_node = DoublyNode(data)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def prepend(self, data):
        """앞에 노드 추가"""
        new_node = DoublyNode(data)

        if not self.head:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def to_list(self):
        """리스트로 변환"""
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result

    def __str__(self):
        """문자열 표현"""
        return ' <-> '.join(map(str, self.to_list()))

if __name__ == '__main__':
    print("=== Singly Linked List ===")
    ll = LinkedList()

    # 데이터 추가
    for i in [1, 2, 3, 4, 5]:
        ll.append(i)

    print(f"Original: {ll}")
    print(f"Length: {len(ll)}")
    print(f"Middle element: {ll.get_middle()}")

    # 삽입
    ll.insert_at(2, 10)
    print(f"After inserting 10 at index 2: {ll}")

    # 검색
    print(f"Search for 3: index {ll.search(3)}")

    # 삭제
    ll.delete(10)
    print(f"After deleting 10: {ll}")

    # 뒤집기
    ll.reverse()
    print(f"Reversed: {ll}")

    print("\n=== Doubly Linked List ===")
    dll = DoublyLinkedList()

    for i in [10, 20, 30, 40]:
        dll.append(i)

    print(f"Doubly Linked List: {dll}")
    dll.prepend(5)
    print(f"After prepending 5: {dll}")
