"""
44. 2048 Game - 2048 게임
"""
import random
import copy

class Game2048:
    def __init__(self, size=4):
        """2048 게임 초기화"""
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """새 타일 추가 (2 또는 4)"""
        empty_cells = [(i, j) for i in range(self.size)
                      for j in range(self.size) if self.board[i][j] == 0]

        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def compress(self, row):
        """0을 제거하고 왼쪽으로 밀기"""
        new_row = [num for num in row if num != 0]
        new_row += [0] * (self.size - len(new_row))
        return new_row

    def merge(self, row):
        """같은 숫자 합치기"""
        for i in range(self.size - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
        return row

    def move_left(self):
        """왼쪽으로 이동"""
        new_board = []
        changed = False

        for row in self.board:
            compressed = self.compress(row)
            merged = self.merge(compressed)
            final = self.compress(merged)
            new_board.append(final)

            if final != row:
                changed = True

        self.board = new_board
        return changed

    def reverse(self):
        """보드 좌우 반전"""
        self.board = [row[::-1] for row in self.board]

    def transpose(self):
        """보드 전치"""
        self.board = [[self.board[j][i] for j in range(self.size)]
                     for i in range(self.size)]

    def move_right(self):
        """오른쪽으로 이동"""
        self.reverse()
        changed = self.move_left()
        self.reverse()
        return changed

    def move_up(self):
        """위로 이동"""
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        """아래로 이동"""
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def move(self, direction):
        """방향으로 이동"""
        moves = {
            'up': self.move_up,
            'down': self.move_down,
            'left': self.move_left,
            'right': self.move_right
        }

        if direction in moves:
            changed = moves[direction]()
            if changed:
                self.add_new_tile()
            return changed

        return False

    def is_game_over(self):
        """게임 종료 확인"""
        # 빈 칸이 있으면 계속 가능
        for row in self.board:
            if 0 in row:
                return False

        # 인접한 같은 숫자가 있으면 계속 가능
        for i in range(self.size):
            for j in range(self.size):
                if j < self.size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < self.size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False

        return True

    def has_won(self):
        """2048 타일 도달 확인"""
        for row in self.board:
            if 2048 in row:
                return True
        return False

    def print_board(self):
        """보드 출력"""
        print(f"\nScore: {self.score}\n")
        print("+" + "------+" * self.size)

        for row in self.board:
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print("      |", end="")
                else:
                    print(f" {cell:4d} |", end="")
            print()
            print("+" + "------+" * self.size)

        print()

class AI2048:
    """간단한 2048 AI"""

    @staticmethod
    def get_best_move(game):
        """최선의 수 찾기 (간단한 휴리스틱)"""
        moves = ['up', 'down', 'left', 'right']
        best_move = None
        best_score = -1

        for move in moves:
            # 임시 보드로 시뮬레이션
            temp_game = copy.deepcopy(game)
            changed = temp_game.move(move)

            if changed:
                # 빈 칸 수 + 최대 타일 값으로 평가
                empty_cells = sum(row.count(0) for row in temp_game.board)
                max_tile = max(max(row) for row in temp_game.board)
                score = empty_cells * 10 + max_tile

                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move or 'up'

if __name__ == '__main__':
    print("=== 2048 Game (Auto-Play Demo) ===\n")

    game = Game2048()
    ai = AI2048()

    game.print_board()

    move_count = 0
    max_moves = 20

    while not game.is_game_over() and move_count < max_moves:
        # AI가 최선의 수 선택
        move = ai.get_best_move(game)
        game.move(move)

        move_count += 1
        print(f"Move {move_count}: {move.upper()}")
        game.print_board()

        if game.has_won():
            print("🎉 Congratulations! You reached 2048!")
            break

    if game.is_game_over():
        print("💀 Game Over!")

    print(f"\nFinal Score: {game.score}")
    print(f"Max Tile: {max(max(row) for row in game.board)}")

    print("\nNote: For manual play, implement keyboard input")
    print("Controls: w(up) s(down) a(left) d(right)")
