# ai-llm — Claude 기반 RAG 챗봇

내 문서(`.md`, `.txt`)를 검색해서 그 내용을 근거로 답하는 RAG(검색 증강 생성) 챗봇입니다.
답변 생성에는 Anthropic Claude API(`claude-opus-5-5`)를 씁니다.

## 구조

```
.
├── data/docs/              # 검색 대상 문서 (여기에 .md/.txt 를 넣는다)
├── data/index/             # `ingest` 가 만드는 검색 인덱스 (git 제외)
├── src/rag_chatbot/
│   ├── config.py           # .env 설정 로드
│   ├── ingest.py           # 문서 로드 + 청크 분할
│   ├── retriever.py        # BM25 검색기 (인덱스 저장/로드)
│   ├── prompts.py          # 시스템 프롬프트, 컨텍스트 포맷
│   ├── chatbot.py          # 검색 → Claude 호출(스트리밍) → 대화 기록
│   └── cli.py              # `rag-chatbot ingest` / `rag-chatbot chat`
└── tests/                  # pytest (API 호출 없이 실행됨)
```

동작 흐름: **문서 → 청크 분할 → BM25 인덱스 → 질문과 관련된 청크 검색 → 청크를 붙여 Claude 에 질문 → 스트리밍 답변**

## 시작하기

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # ANTHROPIC_API_KEY 입력

rag-chatbot ingest          # data/docs → data/index/index.json
rag-chatbot chat --sources  # 대화 시작 (--sources: 검색 결과·토큰 사용량 표시)
```

대화 중 `/reset` 은 대화 기록을 지우고, `/exit` 는 종료합니다.

## 설정 (.env)

| 변수 | 기본값 | 설명 |
|---|---|---|
| `ANTHROPIC_API_KEY` | — | API 키 (`ant auth login` 프로필이 있으면 생략 가능) |
| `RAG_MODEL` | `claude-opus-5-5` | 사용할 Claude 모델 |
| `RAG_EFFORT` | `medium` | 추론 강도 (`low`/`medium`/`high`/`xhigh`/`max`) |
| `RAG_DOCS_DIR` | `data/docs` | 문서 폴더 |
| `RAG_INDEX_PATH` | `data/index/index.json` | 인덱스 파일 |
| `RAG_CHUNK_SIZE` / `RAG_CHUNK_OVERLAP` | `800` / `100` | 청크 크기·겹침 (글자 수) |
| `RAG_TOP_K` | `4` | 질문당 검색할 청크 수 |

## 설계 메모

- **검색기**: 외부 의존성 없는 BM25(한글 2-gram 포함)로 시작합니다. 의미 검색이 필요하면
  `search(query, top_k)` 인터페이스를 유지한 채 임베딩 + 벡터 DB(Chroma, FAISS 등) 구현으로 교체하면 됩니다.
- **프롬프트 캐싱**: 시스템 프롬프트는 고정, 대화 기록은 덧붙이기만 하고 요청에 자동 캐시
  (`cache_control`)를 걸어 두 번째 질문부터 이전 대화가 캐시로 읽힙니다.
- **거절 대응**: 서버 측 fallback(`fallbacks="default"`, beta `server-side-fallback-2026-07-01`)을
  켜 두었습니다. 안전 분류기가 요청을 거절하면 서버가 권장 모델로 다시 실행합니다.
  Bedrock·Vertex·Foundry 에서는 이 파라미터가 지원되지 않으니 제거하세요.

## 테스트

```bash
pytest
ruff check . && ruff format --check .
```
