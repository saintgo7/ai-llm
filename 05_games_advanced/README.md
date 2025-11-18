# 🎮 게임 & 고급 프로젝트

이 폴더에는 게임 및 고급 컴퓨터 과학 프로젝트 10개가 포함되어 있습니다.

> **📚 전체 사용 설명서**: 상세한 한글 가이드는 [사용설명서.md](./사용설명서.md)를 참조하세요.

## 📋 프로그램 목록

### 41. 틱택토
**파일**: `41_tic_tac_toe.py`

절대 지지 않는 AI가 포함된 틱택토 게임입니다.

**주요 기능**:
- Minimax 알고리즘
- AI 상대
- 콘솔 인터페이스
- 게임 상태 추적

**실행 방법**:
```bash
python 41_tic_tac_toe.py
```

**Minimax 알고리즘 이해**:
```python
def minimax(board, depth, is_maximizing):
    """
    Minimax 알고리즘으로 최적의 수를 찾습니다.
    - is_maximizing=True: AI 차례 (점수 최대화)
    - is_maximizing=False: 플레이어 차례 (점수 최소화)
    """
    winner = check_winner(board)
    if winner == 'O':  # AI 승리
        return 10 - depth
    elif winner == 'X':  # 플레이어 승리
        return depth - 10
    elif is_board_full(board):
        return 0  # 무승부

    if is_maximizing:
        best_score = -float('inf')
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score
```

---

### 42. 스네이크 게임
**파일**: `42_snake_game.py`

클래식 스네이크 게임입니다.

**주요 기능**:
- 콘솔 그래픽
- 자동 플레이 모드
- 점수 추적
- 충돌 감지

**실행 방법**:
```bash
python 42_snake_game.py
```

**게임 로직**:
```python
class SnakeGame:
    def move(self, direction):
        """뱀 이동 및 충돌 체크"""
        head_x, head_y = self.snake[0]

        # 새로운 머리 위치 계산
        if direction == 'UP':
            new_head = (head_x - 1, head_y)
        elif direction == 'DOWN':
            new_head = (head_x + 1, head_y)
        elif direction == 'LEFT':
            new_head = (head_x, head_y - 1)
        elif direction == 'RIGHT':
            new_head = (head_x, head_y + 1)

        # 벽 충돌 체크
        if self.is_collision(new_head):
            return False  # 게임 오버

        # 음식 먹기
        if new_head == self.food:
            self.score += 10
            self.snake.insert(0, new_head)
            self.place_food()
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()  # 꼬리 제거

        return True
```

---

### 43. 행맨
**파일**: `43_hangman.py`

단어 맞추기 게임입니다.

**주요 기능**:
- ASCII 아트
- 단어 카테고리
- 힌트 시스템
- 난이도 레벨

**실행 방법**:
```bash
python 43_hangman.py
```

**게임 상태 관리**:
```python
class Hangman:
    def __init__(self, word):
        self.word = word.upper()
        self.guessed = set()
        self.attempts = 6
        self.current_state = ['_'] * len(word)

    def guess(self, letter):
        letter = letter.upper()
        if letter in self.guessed:
            return "이미 시도한 글자입니다."

        self.guessed.add(letter)

        if letter in self.word:
            # 정답 업데이트
            for i, char in enumerate(self.word):
                if char == letter:
                    self.current_state[i] = letter
            return "정답!"
        else:
            self.attempts -= 1
            return f"틀렸습니다. 남은 기회: {self.attempts}"

    def is_won(self):
        return '_' not in self.current_state

    def is_lost(self):
        return self.attempts == 0
```

---

### 44. 2048 게임
**파일**: `44_2048_game.py`

AI 솔버가 포함된 2048 퍼즐 게임입니다.

**주요 기능**:
- 완전한 게임 로직
- AI 솔버
- 이동 검증
- 점수 추적

**실행 방법**:
```bash
python 44_2048_game.py
```

**게임 메커니즘**:
```python
class Game2048:
    def move_left(self):
        """왼쪽으로 타일 이동 및 병합"""
        moved = False
        for row in range(4):
            # 0이 아닌 타일만 수집
            tiles = [self.board[row][col] for col in range(4) if self.board[row][col] != 0]

            # 인접한 같은 숫자 병합
            merged = []
            i = 0
            while i < len(tiles):
                if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                    merged.append(tiles[i] * 2)
                    self.score += tiles[i] * 2
                    i += 2
                else:
                    merged.append(tiles[i])
                    i += 1

            # 0으로 패딩
            merged += [0] * (4 - len(merged))

            # 보드 업데이트
            for col in range(4):
                if self.board[row][col] != merged[col]:
                    moved = True
                self.board[row][col] = merged[col]

        return moved
```

**AI 솔버**:
```python
def expectimax(board, depth):
    """Expectimax 알고리즘으로 최적 이동 찾기"""
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)

    if is_player_turn:
        max_score = 0
        for move in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            new_board = apply_move(board, move)
            score = expectimax(new_board, depth - 1)
            max_score = max(max_score, score)
        return max_score
    else:  # 랜덤 타일 생성
        avg_score = 0
        empty_cells = get_empty_cells(board)
        for cell in empty_cells:
            for value in [2, 4]:
                new_board = place_tile(board, cell, value)
                prob = 0.9 if value == 2 else 0.1
                avg_score += prob * expectimax(new_board, depth - 1)
        return avg_score / len(empty_cells)
```

---

### 45. 스도쿠 솔버
**파일**: `45_sudoku_solver.py`

스도쿠 솔버 및 생성기입니다.

**주요 기능**:
- 백트래킹 솔버
- 퍼즐 생성기
- 난이도 레벨
- 검증

**실행 방법**:
```bash
python 45_sudoku_solver.py
```

**백트래킹 알고리즘**:
```python
def solve_sudoku(board):
    """백트래킹으로 스도쿠 해결"""
    # 빈 칸 찾기
    empty = find_empty(board)
    if not empty:
        return True  # 완성!

    row, col = empty

    # 1-9 시도
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            # 재귀적으로 해결 시도
            if solve_sudoku(board):
                return True

            # 실패 시 백트래킹
            board[row][col] = 0

    return False  # 해결 불가

def is_valid(board, row, col, num):
    """숫자 배치가 유효한지 확인"""
    # 같은 행 체크
    if num in board[row]:
        return False

    # 같은 열 체크
    if num in [board[r][col] for r in range(9)]:
        return False

    # 3x3 박스 체크
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True
```

---

### 46. 체스 엔진
**파일**: `46_chess_engine.py`

간단한 체스 엔진입니다.

**주요 기능**:
- 모든 말의 이동
- 이동 검증
- 유니코드 말
- 캡처 로직

**실행 방법**:
```bash
python 46_chess_engine.py
```

**말 이동 규칙**:
```python
class ChessEngine:
    def get_valid_moves(self, piece, pos):
        """각 말의 유효한 이동 반환"""
        row, col = pos
        moves = []

        if piece == 'P':  # 폰
            # 앞으로 1칸
            if self.board[row-1][col] == ' ':
                moves.append((row-1, col))
            # 첫 이동 시 2칸
            if row == 6 and self.board[row-2][col] == ' ':
                moves.append((row-2, col))
            # 대각선 캡처
            if col > 0 and self.is_enemy(row-1, col-1):
                moves.append((row-1, col-1))
            if col < 7 and self.is_enemy(row-1, col+1):
                moves.append((row-1, col+1))

        elif piece == 'R':  # 룩
            # 가로/세로 이동
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                moves.extend(self.get_line_moves(pos, dr, dc))

        elif piece == 'N':  # 나이트
            knight_moves = [
                (-2,-1), (-2,1), (-1,-2), (-1,2),
                (1,-2), (1,2), (2,-1), (2,1)
            ]
            for dr, dc in knight_moves:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    if not self.is_friendly(new_row, new_col):
                        moves.append((new_row, new_col))

        # ... 다른 말들

        return moves
```

---

### 47. 미로 생성기
**파일**: `47_maze_generator.py`

알고리즘 기반 미로 생성 도구입니다.

**알고리즘**:
- 깊이 우선 탐색 (DFS)
- 재귀 분할
- BFS 솔버
- 경로 시각화

**실행 방법**:
```bash
python 47_maze_generator.py
```

**DFS 미로 생성**:
```python
def generate_maze_dfs(width, height):
    """DFS로 미로 생성"""
    # 모든 벽으로 초기화
    maze = [[1] * width for _ in range(height)]

    def carve_path(x, y):
        maze[y][x] = 0  # 현재 위치를 길로

        # 방향 무작위 섞기
        directions = [(0,2), (2,0), (0,-2), (-2,0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                # 중간 벽 제거
                maze[y + dy//2][x + dx//2] = 0
                carve_path(nx, ny)

    carve_path(1, 1)
    return maze

# BFS로 최단 경로 찾기
def solve_maze_bfs(maze, start, end):
    from collections import deque

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and
                maze[ny][nx] == 0 and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return None  # 경로 없음
```

---

### 48. 정규식 엔진
**파일**: `48_regex_engine.py`

간단한 정규식 엔진입니다.

**주요 기능**:
- 문자 매칭
- 와일드카드 (.)
- 수량자 (*, +, ?)
- 앵커 (^, $)
- 검색 및 치환

**실행 방법**:
```bash
python 48_regex_engine.py
```

**패턴 매칭 구현**:
```python
class RegexEngine:
    def match(self, pattern, text):
        """패턴과 텍스트 매칭"""
        if not pattern:
            return not text

        # 첫 문자 매칭
        first_match = bool(text) and (pattern[0] == text[0] or pattern[0] == '.')

        # 수량자 처리
        if len(pattern) >= 2 and pattern[1] == '*':
            # * : 0번 이상 반복
            return (self.match(pattern[2:], text) or  # 0번 매칭
                   (first_match and self.match(pattern, text[1:])))  # 1번+ 매칭

        elif len(pattern) >= 2 and pattern[1] == '+':
            # + : 1번 이상 반복
            return first_match and (
                self.match(pattern[2:], text[1:]) or  # 정확히 1번
                self.match(pattern, text[1:]))  # 2번 이상

        elif len(pattern) >= 2 and pattern[1] == '?':
            # ? : 0번 또는 1번
            return (self.match(pattern[2:], text) or  # 0번
                   (first_match and self.match(pattern[2:], text[1:])))  # 1번

        else:
            # 일반 매칭
            return first_match and self.match(pattern[1:], text[1:])
```

---

### 49. 마크다운 파서
**파일**: `49_markdown_parser.py`

AST를 생성하는 마크다운 파서입니다.

**주요 기능**:
- AST 생성
- 헤더, 리스트, 코드
- 굵게, 기울임, 링크
- 트리 구조
- JSON 내보내기

**실행 방법**:
```bash
python 49_markdown_parser.py
```

**토큰화 및 파싱**:
```python
class MarkdownParser:
    def parse(self, markdown_text):
        """마크다운을 AST로 파싱"""
        lines = markdown_text.split('\n')
        ast = {'type': 'document', 'children': []}

        i = 0
        while i < len(lines):
            line = lines[i]

            # 헤더
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                text = line.lstrip('#').strip()
                ast['children'].append({
                    'type': 'heading',
                    'level': level,
                    'text': text
                })

            # 코드 블록
            elif line.startswith('```'):
                lang = line[3:].strip()
                code_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                ast['children'].append({
                    'type': 'code',
                    'lang': lang,
                    'code': '\n'.join(code_lines)
                })

            # 리스트
            elif line.startswith('- ') or line.startswith('* '):
                items = []
                while i < len(lines) and (lines[i].startswith('- ') or lines[i].startswith('* ')):
                    items.append(lines[i][2:].strip())
                    i += 1
                i -= 1
                ast['children'].append({
                    'type': 'list',
                    'items': items
                })

            # 단락
            elif line.strip():
                ast['children'].append({
                    'type': 'paragraph',
                    'text': self.parse_inline(line)
                })

            i += 1

        return ast

    def parse_inline(self, text):
        """인라인 요소 파싱 (굵게, 기울임, 링크)"""
        # **굵게**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # *기울임*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # [링크](url)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        return text
```

---

### 50. 컴파일러
**파일**: `50_compiler.py`

간단한 프로그래밍 언어 컴파일러입니다.

**구성 요소**:
- 렉서 (토큰화)
- 파서 (AST 생성)
- 인터프리터 (실행)
- 변수 및 표현식
- 제어문 (if/else)
- print 문

**실행 방법**:
```bash
python 50_compiler.py
```

**컴파일러 구현**:
```python
# 1. 렉서 (Lexer)
class Lexer:
    def tokenize(self, code):
        """코드를 토큰으로 분해"""
        tokens = []
        patterns = [
            ('NUMBER', r'\d+'),
            ('PLUS', r'\+'),
            ('MINUS', r'-'),
            ('MULTIPLY', r'\*'),
            ('DIVIDE', r'/'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('IF', r'if'),
            ('ELSE', r'else'),
            ('PRINT', r'print'),
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('ASSIGN', r'='),
            ('COMPARE', r'==|!=|<=|>=|<|>'),
            ('WHITESPACE', r'\s+'),
        ]

        combined_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patterns)
        for match in re.finditer(combined_pattern, code):
            token_type = match.lastgroup
            value = match.group()
            if token_type != 'WHITESPACE':
                tokens.append((token_type, value))

        return tokens

# 2. 파서 (Parser)
class Parser:
    def parse(self, tokens):
        """토큰을 AST로 변환"""
        self.tokens = tokens
        self.pos = 0
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.parse_statement())
        return {'type': 'program', 'body': statements}

    def parse_statement(self):
        token_type, value = self.current_token()

        if token_type == 'IF':
            return self.parse_if()
        elif token_type == 'PRINT':
            return self.parse_print()
        elif token_type == 'IDENTIFIER':
            return self.parse_assignment()

    def parse_expression(self):
        """수식 파싱"""
        left = self.parse_term()

        while self.current_token()[0] in ['PLUS', 'MINUS']:
            op = self.consume()[1]
            right = self.parse_term()
            left = {'type': 'binary_op', 'op': op, 'left': left, 'right': right}

        return left

# 3. 인터프리터 (Interpreter)
class Interpreter:
    def __init__(self):
        self.variables = {}

    def execute(self, ast):
        """AST 실행"""
        if ast['type'] == 'program':
            for statement in ast['body']:
                self.execute(statement)

        elif ast['type'] == 'assignment':
            name = ast['name']
            value = self.evaluate(ast['value'])
            self.variables[name] = value

        elif ast['type'] == 'print':
            value = self.evaluate(ast['expression'])
            print(value)

        elif ast['type'] == 'if':
            condition = self.evaluate(ast['condition'])
            if condition:
                self.execute(ast['then'])
            elif 'else' in ast:
                self.execute(ast['else'])

    def evaluate(self, node):
        """표현식 평가"""
        if node['type'] == 'number':
            return int(node['value'])
        elif node['type'] == 'identifier':
            return self.variables.get(node['name'], 0)
        elif node['type'] == 'binary_op':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
            op = node['op']
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left // right
```

**예제 프로그램**:
```
x = 10
y = 20
sum = x + y
print sum

if sum > 25
    print 100
else
    print 0
```

---

## ⚡ 빠른 시작

### 1. 프로그램 실행
```bash
cd 05_games_advanced
python 41_tic_tac_toe.py
```

### 2. AI와 대결
```bash
python 41_tic_tac_toe.py  # 틱택토
python 44_2048_game.py     # 2048 AI 관전
```

### 3. 컴파일러 실험
```bash
python 50_compiler.py
```

## 🎓 복잡도 레벨

### 초급 - 게임 기초
1. **틱택토** (41) - Minimax 알고리즘
2. **스네이크** (42) - 게임 루프
3. **행맨** (43) - 상태 관리

### 중급 - 게임 AI
4. **2048** (44) - Expectimax 알고리즘
5. **스도쿠** (45) - 백트래킹
6. **미로** (47) - 그래프 탐색

### 고급 - 컴퓨터 과학
7. **체스** (46) - 복잡한 규칙
8. **정규식 엔진** (48) - 패턴 매칭
9. **마크다운 파서** (49) - AST 생성
10. **컴파일러** (50) - 렉서/파서/인터프리터

## 🎮 게임 AI 알고리즘

### Minimax (틱택토)
- **개념**: 모든 가능한 수를 탐색하여 최적의 수 선택
- **시간 복잡도**: O(b^d) - b=분기율, d=깊이
- **적용**: 2인 완전 정보 게임

### Expectimax (2048)
- **개념**: 확률적 요소를 고려한 Minimax
- **특징**: 랜덤 타일 생성 확률 계산
- **적용**: 확률적 요소가 있는 게임

### 백트래킹 (스도쿠, N-퀸)
- **개념**: 가능한 선택을 시도하고 실패 시 되돌아감
- **최적화**: 가지치기로 탐색 공간 축소
- **적용**: 제약 만족 문제

## 🔧 문제 해결

### 재귀 깊이 초과
```python
import sys
sys.setrecursionlimit(10000)
```

### 게임 속도 조절
```python
import time

# 게임 루프에 딜레이 추가
while game_running:
    update_game()
    render()
    time.sleep(0.1)  # 100ms 딜레이
```

### 터미널 화면 지우기
```python
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
```

## 📚 학습 경로

### 1단계: 게임 기초 (1-2주)
- 틱택토로 게임 로직 학습
- 스네이크로 게임 루프 이해
- 행맨으로 상태 관리 연습

### 2단계: 게임 AI (2-3주)
- Minimax 알고리즘 마스터
- Expectimax로 확률 이해
- 백트래킹으로 최적화 기법 학습

### 3단계: 고급 CS 개념 (3-4주)
- 정규식 엔진으로 패턴 매칭
- 파서로 AST 이해
- 컴파일러로 전체 파이프라인 학습

## 🌟 실전 프로젝트 아이디어

### 1. 게임 AI 토너먼트
```python
# 여러 AI 전략 비교
strategies = [
    minimax_ai,
    random_ai,
    heuristic_ai
]

for i, ai1 in enumerate(strategies):
    for ai2 in strategies[i+1:]:
        results = play_tournament(ai1, ai2, games=100)
        print(f"{ai1.name} vs {ai2.name}: {results}")
```

### 2. 커스텀 언어 만들기
```python
# 50_compiler.py를 확장하여
# 함수, 루프, 배열 등 추가

"""
function factorial(n)
    if n <= 1
        return 1
    else
        return n * factorial(n - 1)

print factorial(5)  # 120
"""
```

### 3. 게임 시각화
```python
# pygame으로 게임 GUI 추가
import pygame

class VisualTicTacToe:
    def render(self):
        for row in range(3):
            for col in range(3):
                pygame.draw.rect(screen, WHITE, (col*100, row*100, 100, 100), 2)
                if self.board[row][col] == 'X':
                    self.draw_x(row, col)
                elif self.board[row][col] == 'O':
                    self.draw_o(row, col)
```

## 🎯 코딩 테스트 연관성

### 그래프 알고리즘
- **미로 생성/해결** → BFS/DFS 문제
- **체스 경로** → 최단 거리 문제

### 백트래킹
- **스도쿠** → N-퀸, 순열/조합
- **미로 생성** → 제약 만족 문제

### 동적 프로그래밍
- **게임 AI** → Minimax/Expectimax
- **최적 전략** → 게임 이론

### 문자열 처리
- **정규식** → 패턴 매칭
- **파서** → 문자열 파싱 문제

## 📖 컴퓨터 과학 개념

### 파싱 (Parsing)
- **토큰화**: 문자열 → 토큰
- **구문 분석**: 토큰 → AST
- **적용**: 컴파일러, 데이터 파싱

### 패턴 매칭 (Pattern Matching)
- **정규식**: 문자 패턴 매칭
- **백트래킹**: 실패 시 되돌아가기
- **적용**: 검색, 검증

### 트리 구조 (Tree Structures)
- **AST**: 추상 구문 트리
- **게임 트리**: 가능한 수의 트리
- **적용**: 파싱, 게임 AI

### 상태 머신 (State Machines)
- **게임 상태**: 현재 게임 상황
- **전이**: 행동에 따른 상태 변화
- **적용**: 게임 로직, UI

## 📖 상세 가이드

각 프로그램의 상세한 알고리즘 설명, 최적화 기법, 확장 아이디어는 **[사용설명서.md](./사용설명서.md)**를 참조하세요.

사용설명서에는 다음 내용이 포함되어 있습니다:
- 🎯 알고리즘 상세 해설
- 💡 게임 AI 전략
- 🏆 최적화 기법
- 🔍 컴파일러 이론
- 🚀 고급 확장 아이디어

---

**총 프로그램 수**: 10개 | **카테고리**: 게임 & 고급 프로젝트

**도움이 필요하신가요?** [사용설명서.md](./사용설명서.md)를 확인하거나 이슈를 등록해 주세요!
