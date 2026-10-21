"""명령행 진입점: `rag-chatbot ingest` / `rag-chatbot chat`."""

from __future__ import annotations

import argparse
import sys

import anthropic

from .config import Settings
from .ingest import chunk_documents, load_documents
from .retriever import BM25Retriever


def cmd_ingest(settings: Settings) -> int:
    docs = load_documents(settings.docs_dir)
    if not docs:
        print(f"{settings.docs_dir} 에 .md/.txt 문서가 없습니다.", file=sys.stderr)
        return 1
    chunks = chunk_documents(docs, settings.chunk_size, settings.chunk_overlap)
    BM25Retriever(chunks).save(settings.index_path)
    print(f"문서 {len(docs)}개 → 청크 {len(chunks)}개를 {settings.index_path} 에 저장했습니다.")
    return 0


def cmd_chat(settings: Settings, show_sources: bool) -> int:
    from .chatbot import RAGChatbot

    if not settings.index_path.exists():
        print("인덱스가 없습니다. 먼저 `rag-chatbot ingest` 를 실행하세요.", file=sys.stderr)
        return 1
    bot = RAGChatbot(BM25Retriever.load(settings.index_path), settings)
    print("RAG 챗봇입니다. 종료: /exit, 대화 초기화: /reset")
    while True:
        try:
            question = input("\n질문> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not question:
            continue
        if question in {"/exit", "/quit"}:
            return 0
        if question == "/reset":
            bot.reset()
            print("대화 기록을 지웠습니다.")
            continue
        try:
            for text in bot.ask(question):
                print(text, end="", flush=True)
            print()
        except anthropic.AuthenticationError:
            print("\n인증 실패: ANTHROPIC_API_KEY 를 확인하세요.", file=sys.stderr)
            return 1
        except anthropic.RateLimitError:
            print("\n요청 한도를 초과했습니다. 잠시 후 다시 시도하세요.", file=sys.stderr)
        except anthropic.APIStatusError as e:
            print(f"\nAPI 오류 ({e.status_code}): {e.message}", file=sys.stderr)
        except anthropic.APIConnectionError:
            print("\n네트워크 연결에 실패했습니다.", file=sys.stderr)
        if show_sources and bot.last_sources:
            print("\n[검색된 문서]")
            for chunk, score in bot.last_sources:
                print(f"  - {chunk.id} (score={score:.2f})")
        if show_sources and bot.last_usage is not None:
            u = bot.last_usage
            print(
                f"[토큰] 입력 {u.input_tokens}, 캐시 읽기 {u.cache_read_input_tokens or 0}, "
                f"캐시 쓰기 {u.cache_creation_input_tokens or 0}, 출력 {u.output_tokens}"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rag-chatbot", description="Claude 기반 RAG 챗봇")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("ingest", help="문서를 청크로 나눠 검색 인덱스를 만든다")
    chat = sub.add_parser("chat", help="대화형 챗봇을 실행한다")
    chat.add_argument("--sources", action="store_true", help="검색된 문서와 토큰 사용량 표시")
    args = parser.parse_args(argv)

    settings = Settings.from_env()
    if args.command == "ingest":
        return cmd_ingest(settings)
    return cmd_chat(settings, args.sources)


if __name__ == "__main__":
    sys.exit(main())
