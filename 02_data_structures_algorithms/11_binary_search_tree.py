"""
11. Binary Search Tree - 이진 탐색 트리 구현
"""

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """값 삽입"""
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        """재귀적 삽입"""
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)

    def search(self, value):
        """값 검색"""
        return self._search_recursive(self.root, value)

    def _search_recursive(self, node, value):
        """재귀적 검색"""
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)

    def delete(self, value):
        """값 삭제"""
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        """재귀적 삭제"""
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # 노드를 찾음
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # 두 자식이 있는 경우
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)

        return node

    def _find_min(self, node):
        """최소값 노드 찾기"""
        while node.left:
            node = node.left
        return node

    def inorder_traversal(self):
        """중위 순회 (정렬된 순서)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        """재귀적 중위 순회"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        """전위 순회"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        """재귀적 전위 순회"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        """후위 순회"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        """재귀적 후위 순회"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def height(self):
        """트리의 높이"""
        return self._height_recursive(self.root)

    def _height_recursive(self, node):
        """재귀적 높이 계산"""
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left),
                      self._height_recursive(node.right))

    def size(self):
        """트리의 노드 개수"""
        return self._size_recursive(self.root)

    def _size_recursive(self, node):
        """재귀적 크기 계산"""
        if node is None:
            return 0
        return 1 + self._size_recursive(node.left) + self._size_recursive(node.right)

if __name__ == '__main__':
    # 테스트
    bst = BinarySearchTree()

    # 삽입
    values = [50, 30, 70, 20, 40, 60, 80]
    for value in values:
        bst.insert(value)

    print("Binary Search Tree Demo")
    print(f"Inserted values: {values}")
    print(f"Inorder traversal (sorted): {bst.inorder_traversal()}")
    print(f"Preorder traversal: {bst.preorder_traversal()}")
    print(f"Postorder traversal: {bst.postorder_traversal()}")
    print(f"Tree height: {bst.height()}")
    print(f"Tree size: {bst.size()}")

    # 검색
    print(f"\nSearch 40: {bst.search(40)}")
    print(f"Search 100: {bst.search(100)}")

    # 삭제
    bst.delete(30)
    print(f"\nAfter deleting 30: {bst.inorder_traversal()}")
