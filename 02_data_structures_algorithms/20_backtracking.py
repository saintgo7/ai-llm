"""
20. Backtracking - 백트래킹 알고리즘
"""

class Backtracking:
    @staticmethod
    def n_queens(n):
        """
        N-Queens 문제: N×N 체스판에 N개의 퀸을 서로 공격하지 않도록 배치

        Returns:
            모든 가능한 배치의 리스트
        """
        def is_safe(board, row, col):
            # 같은 열 체크
            for i in range(row):
                if board[i] == col:
                    return False

            # 왼쪽 대각선 체크
            for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
                if board[i] == j:
                    return False

            # 오른쪽 대각선 체크
            for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
                if board[i] == j:
                    return False

            return True

        def solve(board, row):
            if row == n:
                solutions.append(board[:])
                return

            for col in range(n):
                if is_safe(board, row, col):
                    board[row] = col
                    solve(board, row + 1)
                    board[row] = -1

        solutions = []
        solve([-1] * n, 0)
        return solutions

    @staticmethod
    def sudoku_solver(board):
        """
        스도쿠 퍼즐 풀이

        Args:
            board: 9x9 스도쿠 보드 (0은 빈 칸)

        Returns:
            풀이 성공 여부
        """
        def is_valid(board, row, col, num):
            # 행 체크
            if num in board[row]:
                return False

            # 열 체크
            if num in [board[i][col] for i in range(9)]:
                return False

            # 3x3 박스 체크
            box_row, box_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if board[i][j] == num:
                        return False

            return True

        def solve():
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        for num in range(1, 10):
                            if is_valid(board, row, col, num):
                                board[row][col] = num

                                if solve():
                                    return True

                                board[row][col] = 0

                        return False
            return True

        return solve()

    @staticmethod
    def permutations(arr):
        """모든 순열 생성"""
        def backtrack(start):
            if start == len(arr):
                result.append(arr[:])
                return

            for i in range(start, len(arr)):
                arr[start], arr[i] = arr[i], arr[start]
                backtrack(start + 1)
                arr[start], arr[i] = arr[i], arr[start]

        result = []
        backtrack(0)
        return result

    @staticmethod
    def combinations(arr, k):
        """조합 생성"""
        def backtrack(start, current):
            if len(current) == k:
                result.append(current[:])
                return

            for i in range(start, len(arr)):
                current.append(arr[i])
                backtrack(i + 1, current)
                current.pop()

        result = []
        backtrack(0, [])
        return result

    @staticmethod
    def subset_sum(arr, target):
        """
        부분집합 합 문제: 배열의 부분집합 중 합이 target인 것 찾기

        Returns:
            모든 가능한 부분집합
        """
        def backtrack(start, current, current_sum):
            if current_sum == target:
                result.append(current[:])
                return

            if current_sum > target:
                return

            for i in range(start, len(arr)):
                current.append(arr[i])
                backtrack(i + 1, current, current_sum + arr[i])
                current.pop()

        result = []
        backtrack(0, [], 0)
        return result

    @staticmethod
    def word_search(board, word):
        """
        단어 찾기: 2D 보드에서 단어가 존재하는지 확인

        Args:
            board: 2D 문자 배열
            word: 찾을 단어

        Returns:
            단어 존재 여부
        """
        def backtrack(row, col, index):
            if index == len(word):
                return True

            if (row < 0 or row >= len(board) or
                col < 0 or col >= len(board[0]) or
                board[row][col] != word[index] or
                (row, col) in visited):
                return False

            visited.add((row, col))

            # 상하좌우 탐색
            found = (backtrack(row + 1, col, index + 1) or
                    backtrack(row - 1, col, index + 1) or
                    backtrack(row, col + 1, index + 1) or
                    backtrack(row, col - 1, index + 1))

            visited.remove((row, col))
            return found

        visited = set()
        for i in range(len(board)):
            for j in range(len(board[0])):
                if backtrack(i, j, 0):
                    return True
        return False

    @staticmethod
    def generate_parentheses(n):
        """
        올바른 괄호 조합 생성

        Args:
            n: 괄호 쌍의 개수

        Returns:
            모든 올바른 괄호 조합
        """
        def backtrack(current, open_count, close_count):
            if len(current) == 2 * n:
                result.append(current)
                return

            if open_count < n:
                backtrack(current + '(', open_count + 1, close_count)

            if close_count < open_count:
                backtrack(current + ')', open_count, close_count + 1)

        result = []
        backtrack('', 0, 0)
        return result

    @staticmethod
    def palindrome_partitioning(s):
        """
        문자열을 회문으로 분할하는 모든 방법 찾기

        Returns:
            모든 가능한 분할
        """
        def is_palindrome(sub):
            return sub == sub[::-1]

        def backtrack(start, current):
            if start == len(s):
                result.append(current[:])
                return

            for end in range(start + 1, len(s) + 1):
                substring = s[start:end]
                if is_palindrome(substring):
                    current.append(substring)
                    backtrack(end, current)
                    current.pop()

        result = []
        backtrack(0, [])
        return result

    @staticmethod
    def knight_tour(n):
        """
        나이트 투어: 체스판에서 나이트가 모든 칸을 한 번씩 방문

        Args:
            n: 체스판 크기 (n×n)

        Returns:
            투어 경로 (성공 시) 또는 None
        """
        board = [[-1 for _ in range(n)] for _ in range(n)]

        # 나이트의 이동 가능한 방향
        moves = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                (-2, -1), (-1, -2), (1, -2), (2, -1)]

        def is_safe(x, y):
            return 0 <= x < n and 0 <= y < n and board[x][y] == -1

        def solve(x, y, move_count):
            board[x][y] = move_count

            if move_count == n * n - 1:
                return True

            for dx, dy in moves:
                next_x, next_y = x + dx, y + dy
                if is_safe(next_x, next_y):
                    if solve(next_x, next_y, move_count + 1):
                        return True

            board[x][y] = -1
            return False

        if solve(0, 0, 0):
            return board
        return None

if __name__ == '__main__':
    bt = Backtracking()

    print("=== Backtracking Examples ===\n")

    # N-Queens
    print("1. N-Queens (4×4):")
    solutions = bt.n_queens(4)
    print(f"   Found {len(solutions)} solutions")
    if solutions:
        print(f"   First solution: {solutions[0]}")

    # 순열
    print("\n2. Permutations of [1, 2, 3]:")
    perms = bt.permutations([1, 2, 3])
    print(f"   {perms}")

    # 조합
    print("\n3. Combinations of [1, 2, 3, 4] choose 2:")
    combs = bt.combinations([1, 2, 3, 4], 2)
    print(f"   {combs}")

    # 부분집합 합
    print("\n4. Subset Sum ([2, 3, 5, 7], target=10):")
    subsets = bt.subset_sum([2, 3, 5, 7], 10)
    print(f"   {subsets}")

    # 단어 찾기
    print("\n5. Word Search:")
    board = [
        ['A', 'B', 'C', 'E'],
        ['S', 'F', 'C', 'S'],
        ['A', 'D', 'E', 'E']
    ]
    word = "ABCCED"
    print(f"   Board: {board}")
    print(f"   Word '{word}' exists: {bt.word_search(board, word)}")

    # 괄호 생성
    print("\n6. Generate Parentheses (n=3):")
    parens = bt.generate_parentheses(3)
    print(f"   {parens}")

    # 회문 분할
    print("\n7. Palindrome Partitioning ('aab'):")
    partitions = bt.palindrome_partitioning('aab')
    print(f"   {partitions}")

    # 스도쿠
    print("\n8. Sudoku Solver:")
    sudoku = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    if bt.sudoku_solver(sudoku):
        print("   Solved!")
        for row in sudoku[:3]:  # 처음 3줄만 출력
            print(f"   {row}")
    else:
        print("   No solution found")
