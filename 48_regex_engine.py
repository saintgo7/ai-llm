"""
48. Regex Engine - 간단한 정규표현식 엔진
"""

class SimpleRegex:
    """간단한 정규표현식 엔진"""

    @staticmethod
    def match_char(pattern, text):
        """단일 문자 매칭"""
        if not pattern:
            return True
        if not text:
            return False

        # 특수 문자
        if pattern[0] == '.':
            return True
        if pattern[0] == text[0]:
            return True

        return False

    @classmethod
    def match(cls, pattern, text):
        """정규표현식 매칭"""
        if not pattern:
            return True

        # $ (문자열 끝)
        if pattern == '$':
            return not text

        # ^ (문자열 시작)
        if pattern[0] == '^':
            return cls.match_here(pattern[1:], text)

        # 문자열의 어느 위치에서든 매칭 시도
        while text:
            if cls.match_here(pattern, text):
                return True
            text = text[1:]

        return cls.match_here(pattern, text)

    @classmethod
    def match_here(cls, pattern, text):
        """현재 위치에서 매칭"""
        if not pattern:
            return True

        # * (0개 이상)
        if len(pattern) >= 2 and pattern[1] == '*':
            return cls.match_star(pattern[0], pattern[2:], text)

        # + (1개 이상)
        if len(pattern) >= 2 and pattern[1] == '+':
            if cls.match_char(pattern[0], text):
                return cls.match_star(pattern[0], pattern[2:], text[1:])
            return False

        # ? (0개 또는 1개)
        if len(pattern) >= 2 and pattern[1] == '?':
            if cls.match_here(pattern[2:], text):
                return True
            if text and cls.match_char(pattern[0], text):
                return cls.match_here(pattern[2:], text[1:])
            return False

        # $ (문자열 끝)
        if pattern[0] == '$' and len(pattern) == 1:
            return not text

        # 일반 문자
        if text and cls.match_char(pattern[0], text):
            return cls.match_here(pattern[1:], text[1:])

        return False

    @classmethod
    def match_star(cls, char, pattern, text):
        """* 연산자 처리"""
        # 0개 매칭 시도
        if cls.match_here(pattern, text):
            return True

        # 1개 이상 매칭 시도
        while text and cls.match_char(char, text):
            text = text[1:]
            if cls.match_here(pattern, text):
                return True

        return False

class RegexEngine:
    """고급 정규표현식 엔진"""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, text):
        """매칭 여부 반환"""
        return SimpleRegex.match(self.pattern, text)

    def search(self, text):
        """매칭되는 첫 번째 부분 찾기"""
        for i in range(len(text)):
            if SimpleRegex.match_here(self.pattern, text[i:]):
                # 매칭 끝 찾기
                for j in range(i, len(text) + 1):
                    if SimpleRegex.match_here(self.pattern, text[i:j]) and not SimpleRegex.match_here(self.pattern, text[i:j+1]):
                        return text[i:j]
        return None

    def findall(self, text):
        """매칭되는 모든 부분 찾기"""
        results = []
        i = 0

        while i < len(text):
            if SimpleRegex.match_here(self.pattern, text[i:]):
                # 매칭 끝 찾기
                for j in range(i + 1, len(text) + 1):
                    if not SimpleRegex.match_here(self.pattern, text[i:j]):
                        results.append(text[i:j-1])
                        i = j - 1
                        break
                else:
                    results.append(text[i:])
                    break
            else:
                i += 1

        return results

    def replace(self, text, replacement):
        """매칭되는 부분을 replacement로 치환"""
        result = []
        i = 0

        while i < len(text):
            if SimpleRegex.match_here(self.pattern, text[i:]):
                result.append(replacement)

                # 매칭 끝 찾기
                for j in range(i + 1, len(text) + 1):
                    if not SimpleRegex.match_here(self.pattern, text[i:j]):
                        i = j - 1
                        break
                else:
                    break
            else:
                result.append(text[i])
                i += 1

        return ''.join(result)

# 사용 예제
if __name__ == '__main__':
    print("=== Simple Regex Engine ===\n")

    # 테스트 케이스
    test_cases = [
        ("a", "a", True),
        ("a", "b", False),
        (".", "a", True),
        ("a*", "", True),
        ("a*", "aaa", True),
        ("a*b", "aaab", True),
        ("a+b", "b", False),
        ("a+b", "ab", True),
        ("a+b", "aab", True),
        ("a?b", "b", True),
        ("a?b", "ab", True),
        ("a?b", "aab", False),
        ("^hello", "hello world", True),
        ("world$", "hello world", True),
        ("h.*o", "hello", True),
    ]

    print("Pattern Matching Tests:")
    for pattern, text, expected in test_cases:
        result = SimpleRegex.match(pattern, text)
        status = "✓" if result == expected else "✗"
        print(f"{status} Pattern: '{pattern}' Text: '{text}' -> {result}")

    # 고급 기능
    print("\n=== Advanced Features ===\n")

    # Search
    regex = RegexEngine("a+")
    text = "hello aaa world aa test"
    print(f"Pattern: 'a+' in '{text}'")
    print(f"First match: {regex.search(text)}")

    # Find all
    matches = regex.findall(text)
    print(f"All matches: {matches}")

    # Replace
    result = regex.replace(text, "X")
    print(f"After replace: {result}")

    # 복잡한 패턴
    print("\n=== Complex Patterns ===")

    patterns = [
        ("h.*o", "hello", "Match 'h' followed by anything, ending with 'o'"),
        ("a*b*c", "abc", "Zero or more 'a', then zero or more 'b', then 'c'"),
        ("^start.*end$", "start middle end", "Start with 'start', end with 'end'"),
    ]

    for pattern, text, description in patterns:
        result = SimpleRegex.match(pattern, text)
        print(f"\nPattern: '{pattern}'")
        print(f"Text: '{text}'")
        print(f"Description: {description}")
        print(f"Match: {result}")

    print("\nNote: This is a simplified regex engine for educational purposes")
    print("For production use, use Python's built-in 're' module")
