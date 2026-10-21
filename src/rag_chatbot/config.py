"""환경 변수(.env)에서 설정을 읽는다."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    model: str = "claude-opus-5-5"
    effort: str = "medium"
    max_tokens: int = 64000
    docs_dir: Path = Path("data/docs")
    index_path: Path = Path("data/index/index.json")
    chunk_size: int = 800
    chunk_overlap: int = 100
    top_k: int = 4

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        return cls(
            model=os.getenv("RAG_MODEL", cls.model),
            effort=os.getenv("RAG_EFFORT", cls.effort),
            max_tokens=int(os.getenv("RAG_MAX_TOKENS", cls.max_tokens)),
            docs_dir=Path(os.getenv("RAG_DOCS_DIR", str(cls.docs_dir))),
            index_path=Path(os.getenv("RAG_INDEX_PATH", str(cls.index_path))),
            chunk_size=int(os.getenv("RAG_CHUNK_SIZE", cls.chunk_size)),
            chunk_overlap=int(os.getenv("RAG_CHUNK_OVERLAP", cls.chunk_overlap)),
            top_k=int(os.getenv("RAG_TOP_K", cls.top_k)),
        )
