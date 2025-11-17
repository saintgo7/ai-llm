"""Core modules for NPU detection and inference."""

from .npu_detector import NPUDetector, NPUInfo
from .inference_engine import InferenceEngine

__all__ = ["NPUDetector", "NPUInfo", "InferenceEngine"]
