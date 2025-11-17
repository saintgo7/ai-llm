"""
45. Sudoku Solver - 스도쿠 풀이 프로그램
"""

class SudokuSolver:
    def __init__(self, board):
        """
        스도쿠 솔버 초기화

        Args:
            board: 9x9 스도쿠 보드 (0은 빈 칸)
        """
        self.board = board

    def print_board(self):
        """보드 출력"""
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("------+-------+------")

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")

                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")

    def find_empty(self):
        """빈 칸 찾기"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, num, pos):
        """
        숫자가 유효한지 확인

        Args:
            num: 확인할 숫자
            pos: 위치 (row, col)
        """
        row, col = pos

        # 행 체크
        for j in range(9):
            if self.board[row][j] == num and col != j:
                return False

        # 열 체크
        for i in range(9):
            if self.board[i][col] == num and row != i:
                return False

        # 3x3 박스 체크
        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self):
        """백트래킹으로 스도쿠 풀기"""
        empty = self.find_empty()

        if not empty:
            return True  # 모든 칸이 채워짐

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(num, (row, col)):
                self.board[row][col] = num

                if self.solve():
                    return True

                self.board[row][col] = 0  # 백트래킹

        return False

    def count_solutions(self, limit=2):
        """해의 개수 세기 (최대 limit개까지)"""
        count = [0]

        def solve_count(board):
            if count[0] >= limit:
                return

            empty = None
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        empty = (i, j)
                        break
                if empty:
                    break

            if not empty:
                count[0] += 1
                return

            row, col = empty

            for num in range(1, 10):
                if self.is_valid(num, (row, col)):
                    board[row][col] = num
                    solve_count(board)
                    board[row][col] = 0

        solve_count(self.board)
        return count[0]

class SudokuGenerator:
    """스도쿠 생성기"""

    @staticmethod
    def generate(difficulty='medium'):
        """
        스도쿠 생성

        Args:
            difficulty: 'easy', 'medium', 'hard'
        """
        import random

        # 빈 보드
        board = [[0 for _ in range(9)] for _ in range(9)]

        # 대각선 3x3 박스 채우기
        for box in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)

            for i in range(3):
                for j in range(3):
                    board[box * 3 + i][box * 3 + j] = nums[i * 3 + j]

        # 나머지 채우기
        solver = SudokuSolver(board)
        solver.solve()

        # 난이도에 따라 숫자 제거
        cells_to_remove = {
            'easy': 30,
            'medium': 40,
            'hard': 50
        }.get(difficulty, 40)

        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)

        for i, j in cells[:cells_to_remove]:
            board[i][j] = 0

        return board

if __name__ == '__main__':
    print("=== Sudoku Solver ===\n")

    # 예제 스도쿠 (0은 빈 칸)
    puzzle = [
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

    print("Original Puzzle:")
    solver = SudokuSolver(puzzle)
    solver.print_board()

    print("\nSolving...")
    if solver.solve():
        print("\nSolved Puzzle:")
        solver.print_board()
    else:
        print("\nNo solution exists!")

    # 스도쿠 생성
    print("\n\n=== Sudoku Generator ===\n")
    generator = SudokuGenerator()

    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n{difficulty.capitalize()} Puzzle:")
        new_puzzle = generator.generate(difficulty)
        solver = SudokuSolver(new_puzzle)
        solver.print_board()
