import pytest

from rag_chatbot.ingest import chunk_documents, load_documents, split_text


def test_split_respects_chunk_size():
    text = "\n\n".join(f"문단 {i} " + "가" * 50 for i in range(20))
    chunks = split_text(text, chunk_size=200, overlap=20)
    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)


def test_split_long_paragraph():
    chunks = split_text("a" * 1000, chunk_size=300, overlap=50)
    assert all(len(c) <= 300 for c in chunks)
    assert "".join(chunks).count("a") >= 1000


def test_split_rejects_bad_overlap():
    with pytest.raises(ValueError):
        split_text("abc", chunk_size=10, overlap=10)


def test_load_and_chunk(tmp_path):
    (tmp_path / "a.md").write_text("첫 문서", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.txt").write_text("둘째 문서", encoding="utf-8")
    (tmp_path / "skip.pdf").write_bytes(b"%PDF")
    docs = load_documents(tmp_path)
    assert set(docs) == {"a.md", "sub/b.txt"}
    chunks = chunk_documents(docs, chunk_size=100, overlap=10)
    assert [c.id for c in chunks] == ["a.md#0", "sub/b.txt#0"]
