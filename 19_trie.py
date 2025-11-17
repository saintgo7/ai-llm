"""
19. Trie - 트라이 (접두사 트리) 구현
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0  # 이 노드로 끝나는 단어의 개수

class Trie:
    """트라이 자료구조"""

    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0

    def insert(self, word):
        """단어 삽입"""
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        if not node.is_end_of_word:
            self.word_count += 1

        node.is_end_of_word = True
        node.word_count += 1

    def search(self, word):
        """단어 검색"""
        node = self.root

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.is_end_of_word

    def starts_with(self, prefix):
        """접두사로 시작하는 단어가 있는지 확인"""
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]

        return True

    def delete(self, word):
        """단어 삭제"""
        def _delete_helper(node, word, index):
            if index == len(word):
                if not node.is_end_of_word:
                    return False

                node.is_end_of_word = False
                node.word_count -= 1
                return len(node.children) == 0

            char = word[index]
            if char not in node.children:
                return False

            child_node = node.children[char]
            should_delete_child = _delete_helper(child_node, word, index + 1)

            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        if _delete_helper(self.root, word, 0):
            self.word_count -= 1
            return True
        return False

    def get_all_words_with_prefix(self, prefix):
        """특정 접두사로 시작하는 모든 단어 찾기"""
        node = self.root
        words = []

        # 접두사까지 이동
        for char in prefix:
            if char not in node.children:
                return words
            node = node.children[char]

        # DFS로 모든 단어 찾기
        def dfs(current_node, current_word):
            if current_node.is_end_of_word:
                words.append(current_word)

            for char, child_node in current_node.children.items():
                dfs(child_node, current_word + char)

        dfs(node, prefix)
        return words

    def count_words_with_prefix(self, prefix):
        """특정 접두사로 시작하는 단어 개수"""
        return len(self.get_all_words_with_prefix(prefix))

    def longest_common_prefix(self):
        """모든 단어의 최장 공통 접두사"""
        if self.word_count == 0:
            return ""

        node = self.root
        prefix = ""

        while len(node.children) == 1 and not node.is_end_of_word:
            char = list(node.children.keys())[0]
            prefix += char
            node = node.children[char]

        return prefix

    def get_all_words(self):
        """트라이의 모든 단어 반환"""
        return self.get_all_words_with_prefix("")

    def size(self):
        """저장된 단어 개수"""
        return self.word_count

    def auto_complete(self, prefix, max_suggestions=5):
        """자동완성 제안"""
        suggestions = self.get_all_words_with_prefix(prefix)
        return suggestions[:max_suggestions]

class AutoCompleteSystem:
    """자동완성 시스템 (빈도 기반)"""

    def __init__(self):
        self.trie = Trie()
        self.frequency = {}  # 단어 빈도 저장

    def add_sentence(self, sentence):
        """문장 추가"""
        for word in sentence.lower().split():
            # 구두점 제거
            word = ''.join(c for c in word if c.isalnum())
            if word:
                self.trie.insert(word)
                self.frequency[word] = self.frequency.get(word, 0) + 1

    def suggest(self, prefix, max_suggestions=5):
        """빈도 기반 자동완성 제안"""
        words = self.trie.get_all_words_with_prefix(prefix.lower())

        # 빈도순으로 정렬
        words.sort(key=lambda w: self.frequency.get(w, 0), reverse=True)

        return words[:max_suggestions]

class SpellChecker:
    """간단한 맞춤법 검사기"""

    def __init__(self, dictionary):
        self.trie = Trie()
        for word in dictionary:
            self.trie.insert(word.lower())

    def is_valid(self, word):
        """단어가 사전에 있는지 확인"""
        return self.trie.search(word.lower())

    def suggest_corrections(self, word, max_distance=2):
        """편집 거리 기반 수정 제안"""
        word = word.lower()

        if self.is_valid(word):
            return [word]

        suggestions = []
        all_words = self.trie.get_all_words()

        for dict_word in all_words:
            if self._edit_distance(word, dict_word) <= max_distance:
                suggestions.append(dict_word)

        return suggestions

    def _edit_distance(self, word1, word2):
        """편집 거리 계산"""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        return dp[m][n]

if __name__ == '__main__':
    print("=== Trie Demo ===")
    trie = Trie()

    # 단어 삽입
    words = ["apple", "app", "application", "apply", "banana", "band", "can", "cat"]
    for word in words:
        trie.insert(word)

    print(f"Inserted words: {words}")
    print(f"Total words: {trie.size()}")

    # 검색
    print(f"\nSearch 'app': {trie.search('app')}")
    print(f"Search 'appl': {trie.search('appl')}")

    # 접두사 검색
    print(f"Starts with 'app': {trie.starts_with('app')}")
    print(f"Starts with 'xyz': {trie.starts_with('xyz')}")

    # 접두사로 시작하는 모든 단어
    prefix = "app"
    print(f"\nWords starting with '{prefix}': {trie.get_all_words_with_prefix(prefix)}")

    # 삭제
    trie.delete("app")
    print(f"\nAfter deleting 'app': {trie.get_all_words_with_prefix('app')}")

    # 자동완성
    print(f"\nAuto-complete 'ba': {trie.auto_complete('ba')}")

    print("\n=== Auto-Complete System Demo ===")
    ac = AutoCompleteSystem()

    # 문장 추가
    sentences = [
        "I love programming in Python",
        "Python is a great programming language",
        "I prefer Python over Java",
        "Programming is fun"
    ]

    for sentence in sentences:
        ac.add_sentence(sentence)

    # 제안
    print("Auto-complete suggestions:")
    print(f"  'pro': {ac.suggest('pro')}")
    print(f"  'py': {ac.suggest('py')}")
    print(f"  'i': {ac.suggest('i')}")

    print("\n=== Spell Checker Demo ===")
    dictionary = ["hello", "world", "python", "programming", "algorithm", "data", "structure"]
    checker = SpellChecker(dictionary)

    # 맞춤법 검사
    test_words = ["hello", "helo", "wrld", "python", "pythn"]

    print("Spell checking:")
    for word in test_words:
        is_valid = checker.is_valid(word)
        if is_valid:
            print(f"  '{word}': ✓ Valid")
        else:
            suggestions = checker.suggest_corrections(word)
            print(f"  '{word}': ✗ Invalid - Suggestions: {suggestions}")
