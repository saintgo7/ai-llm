"""
46. Chess Engine - 간단한 체스 엔진
"""

class ChessPiece:
    def __init__(self, color, symbol):
        self.color = color  # 'white' or 'black'
        self.symbol = symbol

    def __str__(self):
        return self.symbol

class Pawn(ChessPiece):
    def __init__(self, color):
        symbol = '♙' if color == 'white' else '♟'
        super().__init__(color, symbol)

class Rook(ChessPiece):
    def __init__(self, color):
        symbol = '♖' if color == 'white' else '♜'
        super().__init__(color, symbol)

class Knight(ChessPiece):
    def __init__(self, color):
        symbol = '♘' if color == 'white' else '♞'
        super().__init__(color, symbol)

class Bishop(ChessPiece):
    def __init__(self, color):
        symbol = '♗' if color == 'white' else '♝'
        super().__init__(color, symbol)

class Queen(ChessPiece):
    def __init__(self, color):
        symbol = '♕' if color == 'white' else '♛'
        super().__init__(color, symbol)

class King(ChessPiece):
    def __init__(self, color):
        symbol = '♔' if color == 'white' else '♚'
        super().__init__(color, symbol)

class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        """초기 체스판 설정"""
        # 폰
        for i in range(8):
            self.board[1][i] = Pawn('black')
            self.board[6][i] = Pawn('white')

        # 룩
        self.board[0][0] = self.board[0][7] = Rook('black')
        self.board[7][0] = self.board[7][7] = Rook('white')

        # 나이트
        self.board[0][1] = self.board[0][6] = Knight('black')
        self.board[7][1] = self.board[7][6] = Knight('white')

        # 비숍
        self.board[0][2] = self.board[0][5] = Bishop('black')
        self.board[7][2] = self.board[7][5] = Bishop('white')

        # 퀸
        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')

        # 킹
        self.board[0][4] = King('black')
        self.board[7][4] = King('white')

    def print_board(self):
        """체스판 출력"""
        print("\n  a b c d e f g h")
        print(" ┌─────────────────┐")

        for i in range(8):
            print(f"{8-i}│", end="")
            for j in range(8):
                piece = self.board[i][j]
                if piece:
                    print(f"{piece} ", end="")
                else:
                    # 체커보드 패턴
                    if (i + j) % 2 == 0:
                        print("· ", end="")
                    else:
                        print("  ", end="")
            print(f"│{8-i}")

        print(" └─────────────────┘")
        print("  a b c d e f g h\n")

    def get_piece(self, pos):
        """위치의 말 가져오기"""
        row, col = pos
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def move_piece(self, from_pos, to_pos):
        """말 이동"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        piece = self.board[from_row][from_col]
        if piece:
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            return True

        return False

    def is_valid_move(self, from_pos, to_pos):
        """유효한 이동인지 확인 (간단한 버전)"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # 범위 체크
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and
                0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        piece = self.board[from_row][from_col]
        if not piece:
            return False

        # 같은 색 말이 있는 곳으로 이동 불가
        target = self.board[to_row][to_col]
        if target and target.color == piece.color:
            return False

        # 각 말의 이동 규칙 (간단한 버전)
        if isinstance(piece, Pawn):
            return self._is_valid_pawn_move(from_pos, to_pos, piece)
        elif isinstance(piece, Rook):
            return self._is_valid_rook_move(from_pos, to_pos)
        elif isinstance(piece, Knight):
            return self._is_valid_knight_move(from_pos, to_pos)
        elif isinstance(piece, Bishop):
            return self._is_valid_bishop_move(from_pos, to_pos)
        elif isinstance(piece, Queen):
            return (self._is_valid_rook_move(from_pos, to_pos) or
                   self._is_valid_bishop_move(from_pos, to_pos))
        elif isinstance(piece, King):
            return abs(to_row - from_row) <= 1 and abs(to_col - from_col) <= 1

        return False

    def _is_valid_pawn_move(self, from_pos, to_pos, piece):
        """폰 이동 규칙"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        direction = -1 if piece.color == 'white' else 1

        # 전진
        if to_col == from_col:
            if to_row == from_row + direction and not self.board[to_row][to_col]:
                return True
            # 첫 이동은 2칸 가능
            start_row = 6 if piece.color == 'white' else 1
            if (from_row == start_row and to_row == from_row + 2 * direction and
                not self.board[to_row][to_col] and not self.board[from_row + direction][to_col]):
                return True

        # 대각선 잡기
        if abs(to_col - from_col) == 1 and to_row == from_row + direction:
            if self.board[to_row][to_col]:
                return True

        return False

    def _is_valid_rook_move(self, from_pos, to_pos):
        """룩 이동 규칙"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # 수직 또는 수평 이동
        if from_row != to_row and from_col != to_col:
            return False

        # 경로에 장애물이 없는지 확인
        return self._is_path_clear(from_pos, to_pos)

    def _is_valid_knight_move(self, from_pos, to_pos):
        """나이트 이동 규칙"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)

        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def _is_valid_bishop_move(self, from_pos, to_pos):
        """비숍 이동 규칙"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        # 대각선 이동
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False

        return self._is_path_clear(from_pos, to_pos)

    def _is_path_clear(self, from_pos, to_pos):
        """경로에 장애물이 없는지 확인"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos

        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)

        current_row, current_col = from_row + row_step, from_col + col_step

        while (current_row, current_col) != (to_row, to_col):
            if self.board[current_row][current_col]:
                return False
            current_row += row_step
            current_col += col_step

        return True

def chess_notation_to_pos(notation):
    """체스 표기법을 좌표로 변환 (예: 'e2' -> (6, 4))"""
    col = ord(notation[0]) - ord('a')
    row = 8 - int(notation[1])
    return (row, col)

if __name__ == '__main__':
    print("=== Simple Chess Engine ===\n")

    board = ChessBoard()
    board.print_board()

    # 예제 이동
    moves = [
        ('e2', 'e4'),  # 백 폰 전진
        ('e7', 'e5'),  # 흑 폰 전진
        ('g1', 'f3'),  # 백 나이트
        ('b8', 'c6'),  # 흑 나이트
    ]

    for from_sq, to_sq in moves:
        from_pos = chess_notation_to_pos(from_sq)
        to_pos = chess_notation_to_pos(to_sq)

        if board.is_valid_move(from_pos, to_pos):
            board.move_piece(from_pos, to_pos)
            print(f"Move: {from_sq} -> {to_sq}")
            board.print_board()
        else:
            print(f"Invalid move: {from_sq} -> {to_sq}")

    print("Note: This is a simplified chess engine for demonstration")
