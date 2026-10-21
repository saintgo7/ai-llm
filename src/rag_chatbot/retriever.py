"""BM25 키워드 검색기.

외부 의존성 없이 바로 돌아가는 기본 구현이다. 벡터 검색(임베딩 + 벡터 DB)으로 바꾸려면
같은 `search(query, top_k)` 인터페이스를 가진 클래스를 만들어 교체하면 된다.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import asdict
from pathlib import Path

from .ingest import Chunk

_TOKEN_RE = re.compile(r"[0-9A-Za-z가-힣]+")


def tokenize(text: str) -> list[str]:
    """소문자 단어 토큰. 한글은 조사 차이를 흡수하도록 글자 2-gram 도 함께 쓴다."""
    tokens: list[str] = []
    for word in _TOKEN_RE.findall(text.lower()):
        tokens.append(word)
        if re.search(r"[가-힣]", word) and len(word) > 2:
            tokens.extend(word[i : i + 2] for i in range(len(word) - 1))
    return tokens


class BM25Retriever:
    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.k1 = k1
        self.b = b
        self._tfs = [Counter(tokenize(c.text)) for c in chunks]
        self._lens = [sum(tf.values()) for tf in self._tfs]
        self._avg_len = (sum(self._lens) / len(self._lens)) if self._lens else 0.0
        df: Counter[str] = Counter()
        for tf in self._tfs:
            df.update(tf.keys())
        n = len(chunks)
        self._idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(self, query: str, top_k: int = 4) -> list[tuple[Chunk, float]]:
        terms = tokenize(query)
        scored: list[tuple[Chunk, float]] = []
        for chunk, tf, length in zip(self.chunks, self._tfs, self._lens, strict=True):
            score = 0.0
            for term in terms:
                freq = tf.get(term)
                if not freq:
                    continue
                norm = self.k1 * (1 - self.b + self.b * length / (self._avg_len or 1))
                score += self._idf[term] * freq * (self.k1 + 1) / (freq + norm)
            if score > 0:
                scored.append((chunk, score))
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(c) for c in self.chunks]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> BM25Retriever:
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls([Chunk(**item) for item in data])
