from rag_chatbot.ingest import Chunk
from rag_chatbot.retriever import BM25Retriever

CHUNKS = [
    Chunk("a#0", "a.md", "RAG는 검색 증강 생성 기법입니다."),
    Chunk("b#0", "b.md", "파이썬은 범용 프로그래밍 언어입니다."),
    Chunk("c#0", "c.md", "Claude 모델은 긴 문맥을 처리할 수 있습니다."),
]


def test_search_ranks_relevant_chunk_first():
    results = BM25Retriever(CHUNKS).search("검색 증강 생성이 뭐야?", top_k=2)
    assert results[0][0].id == "a#0"


def test_search_no_match_returns_empty():
    assert BM25Retriever(CHUNKS).search("zzz", top_k=3) == []


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "index" / "index.json"
    BM25Retriever(CHUNKS).save(path)
    loaded = BM25Retriever.load(path)
    assert loaded.chunks == CHUNKS
    assert loaded.search("파이썬")[0][0].id == "b#0"
