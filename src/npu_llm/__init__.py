"""
NPU-LLM: AI/LLM inference system optimized for NPU (Neural Processing Unit)

This package provides tools for running LLM inference on NPUs using OpenVINO and ONNX Runtime.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .core.npu_detector import NPUDetector, NPUInfo
from .core.inference_engine import InferenceEngine
from .models.model_loader import ModelLoader

__all__ = [
    "NPUDetector",
    "NPUInfo",
    "InferenceEngine",
    "ModelLoader",
]
