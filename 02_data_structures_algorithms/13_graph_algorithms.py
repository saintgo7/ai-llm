"""
13. Graph Algorithms - 그래프 알고리즘 구현
"""
from collections import deque, defaultdict
import heapq

class Graph:
    def __init__(self, directed=False):
        """
        그래프 초기화

        Args:
            directed: True면 방향 그래프, False면 무방향 그래프
        """
        self.graph = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        """간선 추가"""
        self.graph[u].append((v, weight))
        if not self.directed:
            self.graph[v].append((u, weight))

    def bfs(self, start):
        """
        너비 우선 탐색 (BFS)

        Returns:
            방문 순서 리스트
        """
        visited = set()
        queue = deque([start])
        result = []

        visited.add(start)

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start):
        """
        깊이 우선 탐색 (DFS)

        Returns:
            방문 순서 리스트
        """
        visited = set()
        result = []

        def dfs_recursive(vertex):
            visited.add(vertex)
            result.append(vertex)

            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start)
        return result

    def dijkstra(self, start):
        """
        다익스트라 알고리즘 - 최단 경로

        Returns:
            각 노드까지의 최단 거리 딕셔너리
        """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, current = heapq.heappop(pq)

            if current in visited:
                continue

            visited.add(current)

            for neighbor, weight in self.graph[current]:
                distance = current_dist + weight

                if distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

    def bellman_ford(self, start):
        """
        벨만-포드 알고리즘 - 음수 가중치 허용

        Returns:
            (거리 딕셔너리, 음수 사이클 존재 여부)
        """
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        # 모든 간선을 |V| - 1번 반복
        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, weight in self.graph[u]:
                    if distances[u] + weight < distances.get(v, float('inf')):
                        distances[v] = distances[u] + weight

        # 음수 사이클 체크
        for u in self.graph:
            for v, weight in self.graph[u]:
                if distances[u] + weight < distances.get(v, float('inf')):
                    return distances, True  # 음수 사이클 존재

        return distances, False

    def has_cycle(self):
        """사이클 존재 여부 확인"""
        visited = set()
        rec_stack = set()

        def has_cycle_util(vertex, parent):
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    if has_cycle_util(neighbor, vertex):
                        return True
                elif neighbor in rec_stack:
                    if self.directed or neighbor != parent:
                        return True

            rec_stack.remove(vertex)
            return False

        for node in self.graph:
            if node not in visited:
                if has_cycle_util(node, None):
                    return True

        return False

    def topological_sort(self):
        """위상 정렬 (방향 그래프만)"""
        if not self.directed:
            return None

        visited = set()
        stack = []

        def dfs_topo(vertex):
            visited.add(vertex)
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_topo(neighbor)
            stack.append(vertex)

        for node in self.graph:
            if node not in visited:
                dfs_topo(node)

        return stack[::-1]

    def find_connected_components(self):
        """연결 요소 찾기 (무방향 그래프)"""
        visited = set()
        components = []

        def dfs_component(vertex, component):
            visited.add(vertex)
            component.append(vertex)
            for neighbor, _ in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_component(neighbor, component)

        for node in self.graph:
            if node not in visited:
                component = []
                dfs_component(node, component)
                components.append(component)

        return components

    def kruskal_mst(self):
        """크루스칼 알고리즘 - 최소 신장 트리"""
        edges = []
        for u in self.graph:
            for v, weight in self.graph[u]:
                if not self.directed or u < v:
                    edges.append((weight, u, v))

        edges.sort()

        parent = {}
        rank = {}

        def find(node):
            if parent[node] != node:
                parent[node] = find(parent[node])
            return parent[node]

        def union(node1, node2):
            root1 = find(node1)
            root2 = find(node2)

            if root1 != root2:
                if rank[root1] < rank[root2]:
                    parent[root1] = root2
                elif rank[root1] > rank[root2]:
                    parent[root2] = root1
                else:
                    parent[root2] = root1
                    rank[root1] += 1
                return True
            return False

        # 초기화
        for node in self.graph:
            parent[node] = node
            rank[node] = 0

        mst = []
        total_weight = 0

        for weight, u, v in edges:
            if union(u, v):
                mst.append((u, v, weight))
                total_weight += weight

        return mst, total_weight

if __name__ == '__main__':
    # 무방향 그래프 예제
    print("=== Undirected Graph Example ===")
    g = Graph(directed=False)
    g.add_edge('A', 'B', 4)
    g.add_edge('A', 'C', 2)
    g.add_edge('B', 'C', 1)
    g.add_edge('B', 'D', 5)
    g.add_edge('C', 'D', 8)
    g.add_edge('C', 'E', 10)
    g.add_edge('D', 'E', 2)

    print("BFS from A:", g.bfs('A'))
    print("DFS from A:", g.dfs('A'))
    print("Dijkstra from A:", g.dijkstra('A'))
    print("Has cycle:", g.has_cycle())

    mst, total = g.kruskal_mst()
    print(f"Minimum Spanning Tree: {mst}")
    print(f"Total weight: {total}")

    # 방향 그래프 예제
    print("\n=== Directed Graph Example ===")
    dg = Graph(directed=True)
    dg.add_edge('A', 'B')
    dg.add_edge('A', 'C')
    dg.add_edge('B', 'D')
    dg.add_edge('C', 'D')
    dg.add_edge('D', 'E')

    print("Topological Sort:", dg.topological_sort())
