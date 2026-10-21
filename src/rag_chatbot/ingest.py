"""문서를 읽어 청크로 나눈다."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_SUFFIXES = {".md", ".txt"}


@dataclass(frozen=True)
class Chunk:
    id: str
    source: str
    text: str


def load_documents(docs_dir: Path) -> dict[str, str]:
    """docs_dir 아래의 .md/.txt 파일을 {상대경로: 내용} 으로 읽는다."""
    docs: dict[str, str] = {}
    for path in sorted(docs_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            docs[path.relative_to(docs_dir).as_posix()] = path.read_text(encoding="utf-8")
    return docs


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """문단 경계를 우선해 chunk_size 글자 이하로 나누고, 앞 청크 끝부분을 overlap 만큼 겹친다."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not 0 <= overlap < chunk_size:
        raise ValueError("overlap must be in [0, chunk_size)")

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        # 한 문단이 chunk_size 보다 길면 글자 단위로 자른다.
        pieces = (
            [para]
            if len(para) <= chunk_size
            else [para[i : i + chunk_size] for i in range(0, len(para), chunk_size - overlap)]
        )
        for piece in pieces:
            candidate = f"{current}\n\n{piece}" if current else piece
            if len(candidate) <= chunk_size:
                current = candidate
                continue
            if current:
                chunks.append(current)
                tail = current[-overlap:] if overlap else ""
                current = f"{tail}\n\n{piece}" if tail else piece
                if len(current) > chunk_size:
                    current = piece
            else:
                current = piece
    if current:
        chunks.append(current)
    return chunks


def chunk_documents(docs: dict[str, str], chunk_size: int, overlap: int) -> list[Chunk]:
    chunks: list[Chunk] = []
    for source, text in docs.items():
        for i, piece in enumerate(split_text(text, chunk_size, overlap)):
            chunks.append(Chunk(id=f"{source}#{i}", source=source, text=piece))
    return chunks
