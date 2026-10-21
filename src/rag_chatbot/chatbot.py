"""검색 + Claude 호출을 묶은 대화형 RAG 챗봇."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import anthropic

from .config import Settings
from .ingest import Chunk
from .prompts import SYSTEM_PROMPT, build_user_message
from .retriever import BM25Retriever

# 안전 분류기가 요청을 거절하면 서버가 권장 모델로 다시 실행한다.
FALLBACK_BETA = "server-side-fallback-2026-07-01"

# 모델 내부 블록: 응답 중간에 fallback 이 일어나면 경계 이전의 이 블록들은 다시 보내지 않는다.
_INTERNAL_BLOCK_TYPES = {"thinking", "redacted_thinking", "tool_use"}


def history_content(content: list[Any]) -> list[Any]:
    """응답 content 를 대화 기록에 넣을 형태로 정리한다.

    thinking 블록을 포함해 그대로 보내야 한다(수정·삭제하면 이후 요청이 거부될 수 있다).
    예외는 응답 중간 fallback: 마지막 fallback 블록 이전의 내부 블록만 뺀다.
    """
    last_fallback = max(
        (i for i, block in enumerate(content) if block.type == "fallback"), default=-1
    )
    return [
        block
        for i, block in enumerate(content)
        if not (i < last_fallback and block.type in _INTERNAL_BLOCK_TYPES)
    ]


class RAGChatbot:
    def __init__(
        self,
        retriever: BM25Retriever,
        settings: Settings,
        client: anthropic.Anthropic | None = None,
    ):
        self.retriever = retriever
        self.settings = settings
        self.client = client or anthropic.Anthropic()
        # 대화 기록은 덧붙이기만 한다. 앞 턴을 고치면 캐시와 thinking 블록이 무효가 된다.
        self.messages: list[dict[str, Any]] = []
        self.last_sources: list[tuple[Chunk, float]] = []
        self.last_usage: Any = None

    def reset(self) -> None:
        self.messages.clear()

    def ask(self, question: str) -> Iterator[str]:
        """질문에 대한 답변 텍스트를 스트리밍으로 돌려준다."""
        self.last_sources = self.retriever.search(question, top_k=self.settings.top_k)
        self.messages.append(
            {"role": "user", "content": build_user_message(question, self.last_sources)}
        )

        with self.client.beta.messages.stream(
            model=self.settings.model,
            max_tokens=self.settings.max_tokens,
            system=SYSTEM_PROMPT,
            messages=self.messages,
            # 마지막 블록까지 자동 캐시: 다음 턴에서 시스템 프롬프트 + 이전 대화를 캐시로 읽는다.
            cache_control={"type": "ephemeral"},
            output_config={"effort": self.settings.effort},
            betas=[FALLBACK_BETA],
            fallbacks="default",
        ) as stream:
            yield from stream.text_stream
            final = stream.get_final_message()

        self.last_usage = final.usage
        if final.stop_reason == "refusal":
            # 기록에 거절된 턴이 남지 않게 질문을 되돌린다.
            self.messages.pop()
            yield "\n[요청이 거절되었습니다. 질문을 바꿔 다시 시도해 주세요.]"
            return
        self.messages.append({"role": "assistant", "content": history_content(final.content)})
        if final.stop_reason == "max_tokens":
            yield "\n[답변이 최대 토큰 수에 도달해 잘렸습니다.]"
