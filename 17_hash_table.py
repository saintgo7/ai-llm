"""
17. Hash Table - 해시 테이블 구현
"""

class HashTable:
    """체이닝 방식의 해시 테이블"""

    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        """해시 함수"""
        if isinstance(key, str):
            return sum(ord(char) for char in key) % self.size
        return hash(key) % self.size

    def insert(self, key, value):
        """키-값 쌍 삽입"""
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        # 기존 키가 있으면 업데이트
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # 새 키-값 쌍 추가
        bucket.append((key, value))
        self.count += 1

        # 로드 팩터가 0.7을 넘으면 리해싱
        if self.count / self.size > 0.7:
            self._resize()

    def get(self, key):
        """값 조회"""
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        """키-값 쌍 삭제"""
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return v

        raise KeyError(f"Key '{key}' not found")

    def contains(self, key):
        """키 존재 여부 확인"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False

    def keys(self):
        """모든 키 반환"""
        all_keys = []
        for bucket in self.table:
            for k, v in bucket:
                all_keys.append(k)
        return all_keys

    def values(self):
        """모든 값 반환"""
        all_values = []
        for bucket in self.table:
            for k, v in bucket:
                all_values.append(v)
        return all_values

    def items(self):
        """모든 키-값 쌍 반환"""
        all_items = []
        for bucket in self.table:
            all_items.extend(bucket)
        return all_items

    def _resize(self):
        """테이블 크기 재조정"""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def load_factor(self):
        """로드 팩터 계산"""
        return self.count / self.size

    def __len__(self):
        """저장된 항목 개수"""
        return self.count

    def __str__(self):
        """문자열 표현"""
        items = [f"{k}: {v}" for k, v in self.items()]
        return "{" + ", ".join(items) + "}"

class OpenAddressingHashTable:
    """개방 주소법 해시 테이블 (선형 탐사)"""

    def __init__(self, size=100):
        self.size = size
        self.keys = [None] * size
        self.values = [None] * size
        self.count = 0

    def _hash(self, key):
        """해시 함수"""
        if isinstance(key, str):
            return sum(ord(char) for char in key) % self.size
        return hash(key) % self.size

    def _probe(self, index):
        """선형 탐사"""
        return (index + 1) % self.size

    def insert(self, key, value):
        """키-값 쌍 삽입"""
        if self.count / self.size > 0.7:
            self._resize()

        index = self._hash(key)

        # 빈 슬롯을 찾을 때까지 탐사
        while self.keys[index] is not None:
            if self.keys[index] == key:
                # 기존 키 업데이트
                self.values[index] = value
                return
            index = self._probe(index)

        self.keys[index] = key
        self.values[index] = value
        self.count += 1

    def get(self, key):
        """값 조회"""
        index = self._hash(key)
        start_index = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                return self.values[index]
            index = self._probe(index)
            if index == start_index:
                break

        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        """키-값 쌍 삭제 (Lazy deletion)"""
        index = self._hash(key)
        start_index = index

        while self.keys[index] is not None:
            if self.keys[index] == key:
                value = self.values[index]
                self.keys[index] = "__DELETED__"
                self.values[index] = None
                self.count -= 1
                return value
            index = self._probe(index)
            if index == start_index:
                break

        raise KeyError(f"Key '{key}' not found")

    def _resize(self):
        """테이블 크기 재조정"""
        old_keys = self.keys
        old_values = self.values
        self.size *= 2
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

        for i in range(len(old_keys)):
            if old_keys[i] is not None and old_keys[i] != "__DELETED__":
                self.insert(old_keys[i], old_values[i])

    def __len__(self):
        return self.count

# 해시 테이블 응용 예제
def find_duplicates(arr):
    """배열에서 중복 찾기"""
    seen = HashTable()
    duplicates = []

    for item in arr:
        if seen.contains(item):
            if item not in duplicates:
                duplicates.append(item)
        else:
            seen.insert(item, True)

    return duplicates

def two_sum(arr, target):
    """두 수의 합이 target이 되는 쌍 찾기"""
    seen = HashTable()

    for i, num in enumerate(arr):
        complement = target - num
        if seen.contains(complement):
            return [seen.get(complement), i]
        seen.insert(num, i)

    return None

def word_frequency(text):
    """단어 빈도 계산"""
    freq = HashTable()
    words = text.lower().split()

    for word in words:
        # 구두점 제거
        word = ''.join(c for c in word if c.isalnum())
        if word:
            try:
                count = freq.get(word)
                freq.insert(word, count + 1)
            except KeyError:
                freq.insert(word, 1)

    return freq

if __name__ == '__main__':
    print("=== Chaining Hash Table ===")
    ht = HashTable(size=10)

    # 삽입
    ht.insert("apple", 5)
    ht.insert("banana", 7)
    ht.insert("orange", 3)
    ht.insert("grape", 12)

    print(f"Hash Table: {ht}")
    print(f"Length: {len(ht)}")
    print(f"Load Factor: {ht.load_factor():.2f}")

    # 조회
    print(f"\nGet 'apple': {ht.get('apple')}")
    print(f"Contains 'banana': {ht.contains('banana')}")

    # 삭제
    ht.delete("orange")
    print(f"\nAfter deleting 'orange': {ht}")

    # 모든 키와 값
    print(f"\nKeys: {ht.keys()}")
    print(f"Values: {ht.values()}")

    print("\n=== Open Addressing Hash Table ===")
    oaht = OpenAddressingHashTable(size=10)
    oaht.insert("red", 1)
    oaht.insert("blue", 2)
    oaht.insert("green", 3)

    print(f"Get 'blue': {oaht.get('blue')}")
    print(f"Length: {len(oaht)}")

    print("\n=== Applications ===")

    # 중복 찾기
    arr = [1, 2, 3, 4, 2, 5, 6, 3, 7]
    print(f"Duplicates in {arr}: {find_duplicates(arr)}")

    # Two Sum
    arr = [2, 7, 11, 15]
    target = 9
    result = two_sum(arr, target)
    print(f"Two sum ({target}) in {arr}: {result}")

    # 단어 빈도
    text = "the quick brown fox jumps over the lazy dog the fox"
    freq = word_frequency(text)
    print(f"\nWord frequency:")
    for word, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
        print(f"  {word}: {count}")
