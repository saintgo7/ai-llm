"""
43. Hangman - 행맨 게임
"""
import random

class Hangman:
    def __init__(self, word_list=None):
        """
        행맨 게임 초기화

        Args:
            word_list: 단어 목록
        """
        if word_list is None:
            word_list = [
                'python', 'javascript', 'programming', 'computer',
                'algorithm', 'database', 'function', 'variable',
                'framework', 'developer', 'software', 'debugging'
            ]

        self.word_list = word_list
        self.word = random.choice(word_list).upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6

    def get_display_word(self):
        """현재 단어 상태 (맞춘 글자만 표시)"""
        return ' '.join([letter if letter in self.guessed_letters else '_'
                        for letter in self.word])

    def guess(self, letter):
        """글자 추측"""
        letter = letter.upper()

        if letter in self.guessed_letters:
            return "already_guessed"

        self.guessed_letters.add(letter)

        if letter in self.word:
            return "correct"
        else:
            self.wrong_guesses += 1
            return "wrong"

    def is_won(self):
        """게임 승리 여부"""
        return all(letter in self.guessed_letters for letter in self.word)

    def is_lost(self):
        """게임 패배 여부"""
        return self.wrong_guesses >= self.max_wrong_guesses

    def get_hangman_drawing(self):
        """행맨 그림"""
        stages = [
            """
               --------
               |      |
               |
               |
               |
               |
               -
            """,
            """
               --------
               |      |
               |      O
               |
               |
               |
               -
            """,
            """
               --------
               |      |
               |      O
               |      |
               |
               |
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|
               |
               |
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |
               |
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |
               -
            """,
            """
               --------
               |      |
               |      O
               |     \\|/
               |      |
               |     / \\
               -
            """
        ]

        return stages[self.wrong_guesses]

    def play(self):
        """게임 플레이"""
        print("=== Hangman Game ===\n")

        while not self.is_won() and not self.is_lost():
            print(self.get_hangman_drawing())
            print(f"\nWord: {self.get_display_word()}")
            print(f"Guessed letters: {', '.join(sorted(self.guessed_letters))}")
            print(f"Wrong guesses: {self.wrong_guesses}/{self.max_wrong_guesses}")

            guess = input("\nGuess a letter: ").strip()

            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter.")
                continue

            result = self.guess(guess)

            if result == "already_guessed":
                print(f"You already guessed '{guess.upper()}'")
            elif result == "correct":
                print(f"✓ Good guess!")
            else:
                print(f"✗ Wrong guess!")

            print("\n" + "="*40)

        # 게임 종료
        print(self.get_hangman_drawing())
        print(f"\nWord: {self.get_display_word()}")

        if self.is_won():
            print("\n🎉 Congratulations! You won!")
        else:
            print(f"\n💀 Game Over! The word was: {self.word}")

class HangmanWithHints(Hangman):
    """힌트 기능이 있는 행맨"""

    def __init__(self, word_list=None, hints=None):
        super().__init__(word_list)
        self.hints = hints or {}
        self.hints_used = 0
        self.max_hints = 2

    def get_hint(self):
        """힌트 제공"""
        if self.hints_used >= self.max_hints:
            return "No more hints available!"

        # 아직 안 맞춘 글자 중 하나를 힌트로
        unguessed_letters = [letter for letter in set(self.word)
                           if letter not in self.guessed_letters]

        if unguessed_letters:
            hint_letter = random.choice(unguessed_letters)
            self.hints_used += 1
            return f"Hint: The word contains '{hint_letter}'"
        else:
            return "You've already guessed all the letters!"

if __name__ == '__main__':
    # 기본 행맨 게임
    game = Hangman()

    # 자동 플레이 데모
    print("=== Hangman Auto-Play Demo ===\n")
    print(f"Secret word: {game.word} (for demo purposes)")
    print(f"Display: {game.get_display_word()}\n")

    # 몇 개의 추측을 자동으로 시도
    demo_guesses = ['E', 'A', 'R', 'I', 'O', 'T']

    for guess in demo_guesses:
        result = game.guess(guess)
        print(f"Guessing '{guess}': {result}")
        print(f"Display: {game.get_display_word()}")
        print(f"Wrong guesses: {game.wrong_guesses}/{game.max_wrong_guesses}\n")

        if game.is_won():
            print("✓ Won!")
            break
        if game.is_lost():
            print("✗ Lost!")
            break

    # 실제 플레이를 원하면 주석 해제
    # game = Hangman()
    # game.play()

    print("\nNote: Uncomment game.play() to play interactively")
