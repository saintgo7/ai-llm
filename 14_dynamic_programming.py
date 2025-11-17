"""
14. Dynamic Programming - 동적 프로그래밍 알고리즘
"""

class DynamicProgramming:
    @staticmethod
    def fibonacci(n, memo=None):
        """피보나치 수열 (메모이제이션)"""
        if memo is None:
            memo = {}

        if n in memo:
            return memo[n]

        if n <= 1:
            return n

        memo[n] = DynamicProgramming.fibonacci(n-1, memo) + DynamicProgramming.fibonacci(n-2, memo)
        return memo[n]

    @staticmethod
    def fibonacci_tabulation(n):
        """피보나치 수열 (타뷸레이션)"""
        if n <= 1:
            return n

        dp = [0] * (n + 1)
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]

        return dp[n]

    @staticmethod
    def knapsack(weights, values, capacity):
        """
        0/1 배낭 문제

        Args:
            weights: 물건들의 무게 리스트
            values: 물건들의 가치 리스트
            capacity: 배낭 용량

        Returns:
            최대 가치
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        values[i-1] + dp[i-1][w - weights[i-1]],
                        dp[i-1][w]
                    )
                else:
                    dp[i][w] = dp[i-1][w]

        return dp[n][capacity]

    @staticmethod
    def longest_common_subsequence(str1, str2):
        """
        최장 공통 부분 수열 (LCS)

        Returns:
            LCS의 길이와 실제 수열
        """
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # DP 테이블 채우기
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

        # LCS 역추적
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if str1[i-1] == str2[j-1]:
                lcs.append(str1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1

        return dp[m][n], ''.join(reversed(lcs))

    @staticmethod
    def edit_distance(str1, str2):
        """
        편집 거리 (Levenshtein Distance)

        Returns:
            최소 편집 횟수
        """
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # 초기화
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # DP 테이블 채우기
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # 삭제
                        dp[i][j-1],      # 삽입
                        dp[i-1][j-1]     # 교체
                    )

        return dp[m][n]

    @staticmethod
    def coin_change(coins, amount):
        """
        동전 거스름돈 문제

        Args:
            coins: 동전 종류 리스트
            amount: 목표 금액

        Returns:
            최소 동전 개수 (-1이면 불가능)
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for i in range(1, amount + 1):
            for coin in coins:
                if i >= coin:
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1

    @staticmethod
    def longest_increasing_subsequence(arr):
        """
        최장 증가 부분 수열 (LIS)

        Returns:
            LIS의 길이
        """
        if not arr:
            return 0

        n = len(arr)
        dp = [1] * n

        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)

    @staticmethod
    def matrix_chain_multiplication(dimensions):
        """
        행렬 곱셈 순서 최적화

        Args:
            dimensions: 행렬 차원 리스트 [A1_rows, A1_cols=A2_rows, A2_cols, ...]

        Returns:
            최소 곱셈 연산 횟수
        """
        n = len(dimensions) - 1
        dp = [[0] * n for _ in range(n)]

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                dp[i][j] = float('inf')

                for k in range(i, j):
                    cost = (dp[i][k] + dp[k+1][j] +
                           dimensions[i] * dimensions[k+1] * dimensions[j+1])
                    dp[i][j] = min(dp[i][j], cost)

        return dp[0][n-1]

    @staticmethod
    def rod_cutting(prices, length):
        """
        막대 자르기 문제

        Args:
            prices: 각 길이별 가격 리스트 (index 0은 무시)
            length: 막대 길이

        Returns:
            최대 수익
        """
        dp = [0] * (length + 1)

        for i in range(1, length + 1):
            max_val = float('-inf')
            for j in range(1, i + 1):
                if j < len(prices):
                    max_val = max(max_val, prices[j] + dp[i - j])
            dp[i] = max_val

        return dp[length]

    @staticmethod
    def word_break(s, word_dict):
        """
        단어 분할 문제

        Args:
            s: 분할할 문자열
            word_dict: 사용 가능한 단어 집합

        Returns:
            분할 가능 여부
        """
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in word_dict:
                    dp[i] = True
                    break

        return dp[n]

if __name__ == '__main__':
    dp = DynamicProgramming()

    print("=== Dynamic Programming Examples ===\n")

    # 피보나치
    print("1. Fibonacci(10):", dp.fibonacci(10))
    print("   Fibonacci(10) [tabulation]:", dp.fibonacci_tabulation(10))

    # 배낭 문제
    weights = [2, 1, 3, 2]
    values = [12, 10, 20, 15]
    capacity = 5
    print(f"\n2. Knapsack (capacity={capacity}):")
    print(f"   Weights: {weights}, Values: {values}")
    print(f"   Max value: {dp.knapsack(weights, values, capacity)}")

    # LCS
    str1, str2 = "ABCDGH", "AEDFHR"
    length, lcs = dp.longest_common_subsequence(str1, str2)
    print(f"\n3. Longest Common Subsequence:")
    print(f"   String 1: {str1}")
    print(f"   String 2: {str2}")
    print(f"   LCS: {lcs} (length: {length})")

    # 편집 거리
    s1, s2 = "kitten", "sitting"
    print(f"\n4. Edit Distance:")
    print(f"   '{s1}' -> '{s2}': {dp.edit_distance(s1, s2)} operations")

    # 동전 거스름돈
    coins = [1, 2, 5]
    amount = 11
    print(f"\n5. Coin Change:")
    print(f"   Coins: {coins}, Amount: {amount}")
    print(f"   Min coins: {dp.coin_change(coins, amount)}")

    # LIS
    arr = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"\n6. Longest Increasing Subsequence:")
    print(f"   Array: {arr}")
    print(f"   LIS length: {dp.longest_increasing_subsequence(arr)}")

    # 단어 분할
    s = "leetcode"
    word_dict = {"leet", "code"}
    print(f"\n7. Word Break:")
    print(f"   String: '{s}'")
    print(f"   Dictionary: {word_dict}")
    print(f"   Can break: {dp.word_break(s, word_dict)}")
