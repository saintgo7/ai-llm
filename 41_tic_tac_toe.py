"""
41. Tic-Tac-Toe - 틱택토 게임
"""
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

    def print_board(self):
        """보드 출력"""
        print("\n")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---|---|---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---|---|---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("\n")

    def make_move(self, position):
        """수 놓기"""
        if position < 0 or position > 8:
            return False

        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True

        return False

    def check_winner(self):
        """승자 확인"""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 가로
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 세로
            [0, 4, 8], [2, 4, 6]               # 대각선
        ]

        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]
                and self.board[combo[0]] != ' '):
                return self.board[combo[0]]

        return None

    def is_board_full(self):
        """보드가 꽉 찼는지 확인"""
        return ' ' not in self.board

    def switch_player(self):
        """플레이어 변경"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_available_moves(self):
        """가능한 수 목록"""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def minimax(self, is_maximizing):
        """미니맥스 알고리즘 (AI)"""
        winner = self.check_winner()

        if winner == 'O':  # AI 승리
            return 1
        elif winner == 'X':  # 플레이어 승리
            return -1
        elif self.is_board_full():  # 무승부
            return 0

        if is_maximizing:  # AI 차례
            best_score = -float('inf')
            for move in self.get_available_moves():
                self.board[move] = 'O'
                score = self.minimax(False)
                self.board[move] = ' '
                best_score = max(score, best_score)
            return best_score
        else:  # 플레이어 차례
            best_score = float('inf')
            for move in self.get_available_moves():
                self.board[move] = 'X'
                score = self.minimax(True)
                self.board[move] = ' '
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        """AI의 최선의 수"""
        best_score = -float('inf')
        best_move = None

        for move in self.get_available_moves():
            self.board[move] = 'O'
            score = self.minimax(False)
            self.board[move] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def play_vs_ai(self):
        """AI 대전"""
        print("=== Tic-Tac-Toe (vs AI) ===")
        print("Positions: 0-8 (top-left to bottom-right)")

        self.print_board()

        while True:
            if self.current_player == 'X':
                # 플레이어 차례
                try:
                    move = int(input("Your move (0-8): "))
                    if not self.make_move(move):
                        print("Invalid move! Try again.")
                        continue
                except (ValueError, IndexError):
                    print("Please enter a number between 0 and 8.")
                    continue
            else:
                # AI 차례
                print("AI is thinking...")
                move = self.get_best_move()
                self.make_move(move)
                print(f"AI chose position {move}")

            self.print_board()

            # 승자 확인
            winner = self.check_winner()
            if winner:
                print(f"{'You' if winner == 'X' else 'AI'} won!")
                break

            if self.is_board_full():
                print("It's a draw!")
                break

            self.switch_player()

if __name__ == '__main__':
    game = TicTacToe()
    game.play_vs_ai()
