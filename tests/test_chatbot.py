from types import SimpleNamespace

from rag_chatbot.chatbot import RAGChatbot, history_content
from rag_chatbot.config import Settings
from rag_chatbot.ingest import Chunk
from rag_chatbot.prompts import build_user_message
from rag_chatbot.retriever import BM25Retriever


def block(type_, **kw):
    return SimpleNamespace(type=type_, **kw)


def test_build_user_message_includes_sources():
    msg = build_user_message("질문?", [(Chunk("a#0", "a.md", "내용"), 1.0)])
    assert 'source="a.md"' in msg
    assert "<question>\n질문?\n</question>" in msg


def test_history_content_keeps_blocks_without_fallback():
    content = [block("thinking"), block("text", text="hi")]
    assert history_content(content) == content


def test_history_content_drops_internal_blocks_before_fallback():
    thinking, text1, fb, thinking2, text2 = (
        block("thinking"),
        block("text"),
        block("fallback"),
        block("thinking"),
        block("text"),
    )
    assert history_content([thinking, text1, fb, thinking2, text2]) == [
        text1,
        fb,
        thinking2,
        text2,
    ]


class FakeStream:
    def __init__(self, final):
        self.final = final
        self.text_stream = iter(["안녕", "하세요"])

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get_final_message(self):
        return self.final


class FakeClient:
    def __init__(self, final):
        self.calls = []
        messages = SimpleNamespace(stream=self._stream)
        self.beta = SimpleNamespace(messages=messages)
        self._final = final

    def _stream(self, **kwargs):
        self.calls.append(kwargs)
        return FakeStream(self._final)


def make_bot(stop_reason):
    final = SimpleNamespace(
        stop_reason=stop_reason, content=[block("text", text="안녕하세요")], usage=None
    )
    client = FakeClient(final)
    retriever = BM25Retriever([Chunk("a#0", "a.md", "RAG 설명")])
    return RAGChatbot(retriever, Settings(), client=client), client


def test_ask_streams_and_records_history():
    bot, client = make_bot("end_turn")
    assert "".join(bot.ask("RAG 가 뭐야")) == "안녕하세요"
    assert [m["role"] for m in bot.messages] == ["user", "assistant"]
    call = client.calls[0]
    assert call["model"] == "claude-opus-5-5"
    assert call["cache_control"] == {"type": "ephemeral"}
    assert call["fallbacks"] == "default"


def test_ask_refusal_rolls_back_question():
    bot, _ = make_bot("refusal")
    out = "".join(bot.ask("질문"))
    assert "거절" in out
    assert bot.messages == []
