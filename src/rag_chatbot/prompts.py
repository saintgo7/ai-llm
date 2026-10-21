"""시스템 프롬프트와 검색 결과를 붙인 사용자 메시지를 만든다."""

from __future__ import annotations

from .ingest import Chunk

# 프롬프트 캐시가 매 요청 적중하도록 시스템 프롬프트는 고정 문자열로 둔다
# (날짜·요청 ID 같은 바뀌는 값을 넣으면 캐시가 깨진다).
SYSTEM_PROMPT = """\
당신은 사용자가 제공한 문서를 근거로 질문에 답하는 도우미입니다.

- 각 질문과 함께 <documents> 안에 검색된 문서 조각이 주어집니다. 답변은 이 문서들을 근거로 하세요.
- 근거로 쓴 문서는 답변 끝에 [출처: 파일명] 형식으로 밝히세요.
- 문서에 답이 없으면 추측하지 말고 문서에서 찾지 못했다고 말하세요.
  일반 상식으로 보충할 때는 그렇다고 구분해 주세요.
- 사용자가 쓴 언어로 답하세요."""


def format_context(results: list[tuple[Chunk, float]]) -> str:
    if not results:
        return "<documents>\n(검색된 문서 없음)\n</documents>"
    parts = [
        f'<document index="{i}" source="{chunk.source}">\n{chunk.text}\n</document>'
        for i, (chunk, _score) in enumerate(results, start=1)
    ]
    return "<documents>\n" + "\n".join(parts) + "\n</documents>"


def build_user_message(question: str, results: list[tuple[Chunk, float]]) -> str:
    return f"{format_context(results)}\n\n<question>\n{question}\n</question>"
