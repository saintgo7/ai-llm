"""
47. Maze Generator - 미로 생성기
"""
import random

class MazeGenerator:
    def __init__(self, width, height):
        """
        미로 생성기 초기화

        Args:
            width: 미로 너비 (홀수)
            height: 미로 높이 (홀수)
        """
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]

    def generate_dfs(self):
        """깊이 우선 탐색으로 미로 생성"""
        # 시작점
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = 0

        stack = [(start_x, start_y)]
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]  # 상, 우, 하, 좌

        while stack:
            x, y = stack[-1]
            random.shuffle(directions)

            found = False
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if (0 < nx < self.width - 1 and 0 < ny < self.height - 1 and
                    self.maze[ny][nx] == 1):
                    # 벽 제거
                    self.maze[ny][nx] = 0
                    self.maze[y + dy // 2][x + dx // 2] = 0

                    stack.append((nx, ny))
                    found = True
                    break

            if not found:
                stack.pop()

        # 출구 생성
        self.maze[0][1] = 0  # 입구
        self.maze[self.height - 1][self.width - 2] = 0  # 출구

    def generate_recursive_division(self):
        """재귀적 분할로 미로 생성"""
        # 모든 셀을 통로로 초기화
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # 외벽 생성
        for i in range(self.height):
            self.maze[i][0] = 1
            self.maze[i][self.width - 1] = 1

        for j in range(self.width):
            self.maze[0][j] = 1
            self.maze[self.height - 1][j] = 1

        def divide(x, y, width, height):
            if width < 3 or height < 3:
                return

            # 수평 또는 수직 분할
            horizontal = width < height if width != height else random.choice([True, False])

            if horizontal:
                # 수평 벽 생성
                wall_y = y + random.randrange(1, height - 1, 2)
                for i in range(x, x + width):
                    self.maze[wall_y][i] = 1

                # 통로 생성
                passage_x = x + random.randrange(0, width, 2)
                self.maze[wall_y][passage_x] = 0

                # 재귀적으로 분할
                divide(x, y, width, wall_y - y)
                divide(x, wall_y + 1, width, y + height - wall_y - 1)
            else:
                # 수직 벽 생성
                wall_x = x + random.randrange(1, width - 1, 2)
                for i in range(y, y + height):
                    self.maze[i][wall_x] = 1

                # 통로 생성
                passage_y = y + random.randrange(0, height, 2)
                self.maze[passage_y][wall_x] = 0

                # 재귀적으로 분할
                divide(x, y, wall_x - x, height)
                divide(wall_x + 1, y, x + width - wall_x - 1, height)

        divide(1, 1, self.width - 2, self.height - 2)

    def solve_bfs(self, start=(1, 1), end=None):
        """BFS로 미로 해결"""
        from collections import deque

        if end is None:
            end = (self.width - 2, self.height - 2)

        queue = deque([(start, [start])])
        visited = {start}

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == end:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.width and 0 <= ny < self.height and
                    self.maze[ny][nx] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        return None

    def print_maze(self, solution_path=None):
        """미로 출력"""
        path_set = set(solution_path) if solution_path else set()

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in path_set:
                    print('·', end=' ')  # 경로
                elif self.maze[y][x] == 1:
                    print('█', end=' ')  # 벽
                else:
                    print(' ', end=' ')  # 통로
            print()

if __name__ == '__main__':
    print("=== Maze Generator ===\n")

    # 1. DFS 미로
    print("1. DFS Maze (15x15)")
    maze1 = MazeGenerator(15, 15)
    maze1.generate_dfs()
    maze1.print_maze()

    # 해결
    print("\nSolved DFS Maze:")
    solution = maze1.solve_bfs()
    if solution:
        maze1.print_maze(solution)
        print(f"Solution length: {len(solution)} steps")
    else:
        print("No solution found!")

    # 2. 재귀적 분할 미로
    print("\n\n2. Recursive Division Maze (21x21)")
    maze2 = MazeGenerator(21, 21)
    maze2.generate_recursive_division()
    maze2.print_maze()

    # 해결
    print("\nSolved Recursive Division Maze:")
    solution = maze2.solve_bfs()
    if solution:
        maze2.print_maze(solution)
        print(f"Solution length: {len(solution)} steps")
    else:
        print("No solution found!")
