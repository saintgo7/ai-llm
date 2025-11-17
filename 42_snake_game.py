"""
42. Snake Game - 스네이크 게임 (콘솔 버전)
"""
import random
import time
import os

class SnakeGame:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = 'RIGHT'
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

    def generate_food(self):
        """음식 생성"""
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food

    def move(self):
        """뱀 이동"""
        head_x, head_y = self.snake[0]

        if self.direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        else:  # RIGHT
            new_head = (head_x + 1, head_y)

        # 벽 충돌 체크
        if (new_head[0] < 0 or new_head[0] >= self.width or
            new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return

        # 자기 자신 충돌 체크
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # 음식 먹기
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def change_direction(self, new_direction):
        """방향 변경"""
        opposite = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction

    def print_game(self):
        """게임 화면 출력"""
        os.system('clear' if os.name != 'nt' else 'cls')

        print('=' * (self.width + 2))
        for y in range(self.height):
            print('|', end='')
            for x in range(self.width):
                if (x, y) == self.snake[0]:
                    print('O', end='')  # 뱀 머리
                elif (x, y) in self.snake:
                    print('o', end='')  # 뱀 몸통
                elif (x, y) == self.food:
                    print('*', end='')  # 음식
                else:
                    print(' ', end='')
            print('|')
        print('=' * (self.width + 2))
        print(f'Score: {self.score}')
        print('Controls: w(up) s(down) a(left) d(right) q(quit)')

# 간단한 자동 플레이 데모
class AutoSnake(SnakeGame):
    """자동 플레이 스네이크"""

    def get_next_direction(self):
        """음식을 향한 방향"""
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food

        # 간단한 휴리스틱: 음식을 향해 이동
        if abs(food_x - head_x) > abs(food_y - head_y):
            # X축 우선
            if food_x > head_x:
                return 'RIGHT'
            else:
                return 'LEFT'
        else:
            # Y축 우선
            if food_y > head_y:
                return 'DOWN'
            else:
                return 'UP'

    def play_auto(self, max_moves=100):
        """자동 플레이"""
        moves = 0

        while not self.game_over and moves < max_moves:
            self.print_game()
            next_dir = self.get_next_direction()
            self.change_direction(next_dir)
            self.move()
            time.sleep(0.2)
            moves += 1

        self.print_game()
        if self.game_over:
            print("\nGame Over!")
        else:
            print(f"\nReached max moves ({max_moves})")
        print(f"Final Score: {self.score}")

if __name__ == '__main__':
    print("=== Snake Game (Auto Play Demo) ===\n")
    game = AutoSnake(width=15, height=10)
    game.play_auto(max_moves=50)

    print("\nNote: For manual play, you would use keyboard input")
    print("Example: w/a/s/d for movement")
