# NPU-LLM: AI/LLM Inference on NPU

NPU-LLM은 NPU(Neural Processing Unit)를 활용하여 Large Language Model(LLM) 추론을 최적화하는 Python 라이브러리입니다. Intel NPU, AMD XDNA NPU 등 다양한 NPU 하드웨어에서 LLM을 효율적으로 실행할 수 있습니다.

## 주요 기능

- **NPU 자동 감지**: 시스템의 NPU 하드웨어를 자동으로 감지하고 최적의 디바이스 선택
- **다중 백엔드 지원**: OpenVINO와 ONNX Runtime 백엔드 지원
- **HuggingFace 통합**: HuggingFace Hub의 모델을 자동으로 다운로드하고 NPU 형식으로 변환
- **간편한 API**: 고수준 API로 쉽고 빠른 LLM 추론
- **성능 벤치마킹**: 내장된 벤치마킹 도구로 성능 측정

## 시스템 요구사항

- Python 3.9 이상
- NPU 하드웨어 (Intel Core Ultra 프로세서 등) 또는 CPU/GPU
- Linux, Windows 10/11

## 설치

### 기본 설치

```bash
# 저장소 클론
git clone https://github.com/yourusername/npu-llm.git
cd npu-llm

# 의존성 설치
pip install -r requirements.txt

# 또는 개발 의존성 포함 설치
pip install -r requirements-dev.txt
```

### pip를 통한 설치 (개발 모드)

```bash
pip install -e .
```

## 빠른 시작

### 1. NPU 감지

시스템의 NPU를 감지하고 정보를 확인합니다:

```bash
python src/npu_llm/examples/detect_npu.py
```

### 2. 간단한 텍스트 생성

```python
from npu_llm.models.model_loader import ModelLoader
from npu_llm.models.llm_pipeline import LLMPipeline

# 모델 로드 (자동으로 HuggingFace에서 다운로드 및 변환)
loader = ModelLoader()
model_path = loader.load_huggingface_model(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    export_format="openvino"
)

# 추론 파이프라인 생성
pipeline = LLMPipeline(
    model_path=model_path,
    device="NPU",  # 또는 "CPU", "GPU"
    backend="openvino"
)

# 텍스트 생성
response = pipeline.generate(
    prompt="What is artificial intelligence?",
    max_length=100,
    temperature=0.7
)

print(response)
```

### 3. 대화형 채팅

```bash
python src/npu_llm/examples/chat_demo.py --model-id TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

### 4. 명령줄에서 텍스트 생성

```bash
python src/npu_llm/examples/simple_generation.py \
    --model-id TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
    --prompt "Tell me about neural processing units" \
    --max-length 150 \
    --device NPU
```

## 프로젝트 구조

```
npu-llm/
├── src/npu_llm/
│   ├── core/               # 핵심 모듈
│   │   ├── npu_detector.py # NPU 감지
│   │   └── inference_engine.py # 추론 엔진
│   ├── models/             # 모델 관리
│   │   ├── model_loader.py # 모델 로더
│   │   └── llm_pipeline.py # LLM 파이프라인
│   ├── utils/              # 유틸리티
│   │   ├── logger.py       # 로깅
│   │   └── config.py       # 설정 관리
│   └── examples/           # 예제 스크립트
├── configs/                # 설정 파일
├── tests/                  # 테스트
├── docs/                   # 문서
├── requirements.txt        # 의존성
├── pyproject.toml         # 프로젝트 설정
└── README.md              # 이 파일
```

## 설정

### 환경 변수

`.env.example` 파일을 `.env`로 복사하고 수정:

```bash
cp .env.example .env
```

주요 환경 변수:
- `NPU_LLM_CACHE_DIR`: 모델 캐시 디렉토리
- `NPU_LLM_DEVICE`: 기본 디바이스 (NPU, CPU, GPU)
- `NPU_LLM_BACKEND`: 기본 백엔드 (openvino, onnxruntime)
- `NPU_LLM_LOG_LEVEL`: 로그 레벨 (DEBUG, INFO, WARNING, ERROR)

### YAML 설정 파일

`configs/config.yaml`에서 상세 설정 가능:

```yaml
model:
  cache_dir: ~/.cache/npu_llm
  default_backend: openvino
  default_device: NPU

inference:
  max_length: 512
  temperature: 0.7
  top_p: 0.9
  top_k: 50
```

## 고급 사용법

### 로컬 모델 사용

```python
from pathlib import Path
from npu_llm.models.llm_pipeline import LLMPipeline

# 로컬 모델 경로
model_path = Path("/path/to/local/model")

pipeline = LLMPipeline(
    model_path=model_path,
    device="NPU",
    backend="openvino"
)
```

### 성능 벤치마킹

```python
# 성능 측정
metrics = pipeline.benchmark(
    prompt="Test prompt",
    iterations=10
)

print(f"Mean Latency: {metrics['mean_latency']:.3f}s")
print(f"Tokens/sec: {metrics['tokens_per_second']:.2f}")
```

### NPU 정보 프로그래밍 방식으로 확인

```python
from npu_llm.core.npu_detector import NPUDetector

detector = NPUDetector()

if detector.is_npu_available():
    print(f"Found {detector.get_npu_count()} NPU(s)")
    print(f"Best device: {detector.get_best_device()}")

    for npu in detector.npu_devices:
        print(f"  - {npu.name} ({npu.backend})")
else:
    print("No NPU detected, using CPU")
```

## 지원하는 모델

HuggingFace Hub의 대부분의 causal language models를 지원합니다:

- TinyLlama
- Llama 2/3
- Mistral
- Phi
- GPT-2
- 기타 transformers 라이브러리 호환 모델

## 지원하는 NPU

- **Intel NPU**: Intel Core Ultra (Meteor Lake) 이상
- **AMD XDNA NPU**: Ryzen AI 프로세서
- **Qualcomm NPU**: (ONNX Runtime QNN provider를 통해)

NPU가 없는 경우 자동으로 CPU 또는 GPU로 폴백됩니다.

## 개발

### 테스트 실행

```bash
pytest tests/
```

### 코드 포맷팅

```bash
black src/
isort src/
```

### 타입 체크

```bash
mypy src/
```

## 문제 해결

### NPU가 감지되지 않는 경우

1. OpenVINO가 제대로 설치되었는지 확인
2. NPU 드라이버가 설치되어 있는지 확인
3. `python src/npu_llm/examples/detect_npu.py`로 상세 정보 확인

### 모델 변환 오류

- 충분한 디스크 공간이 있는지 확인
- HuggingFace 토큰이 필요한 gated 모델인지 확인
- `optimum[openvino]` 또는 `optimum[onnxruntime]`이 설치되었는지 확인

### 성능 문제

- `performance_hint`를 `LATENCY` 또는 `THROUGHPUT`으로 조정
- 모델 양자화 고려 (INT8)
- 더 작은 모델 사용 고려

## 라이선스

MIT License

## 기여

이슈와 Pull Request를 환영합니다!

## 참고 자료

- [OpenVINO Documentation](https://docs.openvino.ai/)
- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [Optimum Intel](https://huggingface.co/docs/optimum/intel/index)

## 문의

문제나 질문이 있으시면 GitHub Issues를 이용해 주세요.