"""Inference engine for running LLM models on NPU."""

import logging
import time
from typing import Any, Dict, List, Optional, Union

import numpy as np

from .npu_detector import NPUDetector

logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    Main inference engine for running LLM models on NPU.

    Supports OpenVINO and ONNX Runtime backends.
    """

    def __init__(
        self,
        model_path: str,
        device: Optional[str] = None,
        backend: str = "auto",
        **kwargs
    ):
        """
        Initialize the inference engine.

        Args:
            model_path: Path to the model (IR format for OpenVINO, ONNX for ONNX Runtime)
            device: Target device ('NPU', 'CPU', 'GPU', or None for auto-detection)
            backend: Backend to use ('openvino', 'onnxruntime', or 'auto')
            **kwargs: Additional backend-specific parameters
        """
        self.model_path = model_path
        self.backend_type = backend
        self.kwargs = kwargs

        # Detect NPU if device is not specified
        self.detector = NPUDetector()
        if device is None:
            self.device = self.detector.get_best_device()
            logger.info(f"Auto-selected device: {self.device}")
        else:
            self.device = device
            logger.info(f"Using specified device: {self.device}")

        # Select backend
        if backend == "auto":
            self.backend_type = self._select_backend()

        # Initialize model
        self.model = None
        self.compiled_model = None
        self.session = None

        self._load_model()

    def _select_backend(self) -> str:
        """Auto-select the best backend based on available NPUs."""
        if self.detector.npu_devices:
            # Prefer OpenVINO for NPU
            for npu in self.detector.npu_devices:
                if npu.backend == 'openvino':
                    return 'openvino'
            # Fall back to first available backend
            return self.detector.npu_devices[0].backend

        # Default to OpenVINO if no NPU detected
        return 'openvino'

    def _load_model(self) -> None:
        """Load the model using the selected backend."""
        logger.info(f"Loading model from {self.model_path} using {self.backend_type} backend")

        if self.backend_type == 'openvino':
            self._load_openvino_model()
        elif self.backend_type == 'onnxruntime':
            self._load_onnxruntime_model()
        else:
            raise ValueError(f"Unsupported backend: {self.backend_type}")

    def _load_openvino_model(self) -> None:
        """Load model using OpenVINO."""
        try:
            import openvino as ov

            core = ov.Core()

            # Load model
            logger.info(f"Reading model from {self.model_path}")
            self.model = core.read_model(self.model_path)

            # Configure device
            config = self.kwargs.get('config', {})

            # Compile model
            logger.info(f"Compiling model for {self.device}")
            self.compiled_model = core.compile_model(
                self.model,
                device_name=self.device,
                config=config
            )

            logger.info("Model loaded successfully with OpenVINO")

        except ImportError:
            raise RuntimeError("OpenVINO is not installed. Install with: pip install openvino")
        except Exception as e:
            logger.error(f"Error loading OpenVINO model: {e}")
            raise

    def _load_onnxruntime_model(self) -> None:
        """Load model using ONNX Runtime."""
        try:
            import onnxruntime as ort

            # Configure session options
            sess_options = ort.SessionOptions()
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

            # Select providers
            providers = self.kwargs.get('providers', None)
            if providers is None:
                providers = ['CPUExecutionProvider']
                if 'NPU' in self.device:
                    # Try to use NPU provider if available
                    available_providers = ort.get_available_providers()
                    npu_providers = [p for p in available_providers if 'NPU' in p.upper() or 'QNN' in p.upper()]
                    if npu_providers:
                        providers = npu_providers + providers

            logger.info(f"Creating ONNX Runtime session with providers: {providers}")
            self.session = ort.InferenceSession(
                self.model_path,
                sess_options=sess_options,
                providers=providers
            )

            logger.info("Model loaded successfully with ONNX Runtime")

        except ImportError:
            raise RuntimeError("ONNX Runtime is not installed. Install with: pip install onnxruntime")
        except Exception as e:
            logger.error(f"Error loading ONNX Runtime model: {e}")
            raise

    def infer(self, inputs: Union[Dict[str, np.ndarray], List[np.ndarray]]) -> Dict[str, np.ndarray]:
        """
        Run inference on the model.

        Args:
            inputs: Input data (dict of numpy arrays or list of numpy arrays)

        Returns:
            Dictionary of output tensors
        """
        if self.backend_type == 'openvino':
            return self._infer_openvino(inputs)
        elif self.backend_type == 'onnxruntime':
            return self._infer_onnxruntime(inputs)
        else:
            raise ValueError(f"Unsupported backend: {self.backend_type}")

    def _infer_openvino(self, inputs: Union[Dict[str, np.ndarray], List[np.ndarray]]) -> Dict[str, np.ndarray]:
        """Run inference using OpenVINO."""
        if self.compiled_model is None:
            raise RuntimeError("Model is not loaded")

        start_time = time.time()

        # Create infer request
        infer_request = self.compiled_model.create_infer_request()

        # Set inputs
        if isinstance(inputs, dict):
            for name, data in inputs.items():
                infer_request.set_tensor(name, data)
        else:
            for i, data in enumerate(inputs):
                infer_request.set_input_tensor(i, data)

        # Run inference
        infer_request.infer()

        # Get outputs
        outputs = {}
        for output in self.compiled_model.outputs:
            outputs[output.get_any_name()] = infer_request.get_tensor(output).data

        inference_time = time.time() - start_time
        logger.debug(f"Inference completed in {inference_time:.3f}s")

        return outputs

    def _infer_onnxruntime(self, inputs: Union[Dict[str, np.ndarray], List[np.ndarray]]) -> Dict[str, np.ndarray]:
        """Run inference using ONNX Runtime."""
        if self.session is None:
            raise RuntimeError("Model is not loaded")

        start_time = time.time()

        # Prepare inputs
        if isinstance(inputs, list):
            input_names = [inp.name for inp in self.session.get_inputs()]
            inputs = {name: data for name, data in zip(input_names, inputs)}

        # Run inference
        output_names = [out.name for out in self.session.get_outputs()]
        outputs = self.session.run(output_names, inputs)

        # Convert to dictionary
        result = {name: output for name, output in zip(output_names, outputs)}

        inference_time = time.time() - start_time
        logger.debug(f"Inference completed in {inference_time:.3f}s")

        return result

    def get_input_info(self) -> Dict[str, Any]:
        """Get information about model inputs."""
        if self.backend_type == 'openvino':
            if self.model is None:
                return {}
            return {
                inp.get_any_name(): {
                    'shape': inp.get_partial_shape(),
                    'dtype': inp.get_element_type().get_type_name()
                }
                for inp in self.model.inputs
            }
        elif self.backend_type == 'onnxruntime':
            if self.session is None:
                return {}
            return {
                inp.name: {
                    'shape': inp.shape,
                    'dtype': inp.type
                }
                for inp in self.session.get_inputs()
            }
        return {}

    def get_output_info(self) -> Dict[str, Any]:
        """Get information about model outputs."""
        if self.backend_type == 'openvino':
            if self.model is None:
                return {}
            return {
                out.get_any_name(): {
                    'shape': out.get_partial_shape(),
                    'dtype': out.get_element_type().get_type_name()
                }
                for out in self.model.outputs
            }
        elif self.backend_type == 'onnxruntime':
            if self.session is None:
                return {}
            return {
                out.name: {
                    'shape': out.shape,
                    'dtype': out.type
                }
                for out in self.session.get_outputs()
            }
        return {}

    def benchmark(self, inputs: Union[Dict[str, np.ndarray], List[np.ndarray]], iterations: int = 10) -> Dict[str, float]:
        """
        Benchmark inference performance.

        Args:
            inputs: Input data
            iterations: Number of iterations to run

        Returns:
            Performance metrics (mean, min, max latency)
        """
        latencies = []

        logger.info(f"Running benchmark with {iterations} iterations...")

        for i in range(iterations):
            start_time = time.time()
            self.infer(inputs)
            latency = time.time() - start_time
            latencies.append(latency)

        metrics = {
            'mean_latency': np.mean(latencies),
            'min_latency': np.min(latencies),
            'max_latency': np.max(latencies),
            'std_latency': np.std(latencies),
            'throughput': 1.0 / np.mean(latencies)
        }

        logger.info(f"Benchmark results: Mean={metrics['mean_latency']:.3f}s, "
                   f"Min={metrics['min_latency']:.3f}s, Max={metrics['max_latency']:.3f}s")

        return metrics

    def __del__(self):
        """Cleanup resources."""
        self.model = None
        self.compiled_model = None
        self.session = None
