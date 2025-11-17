"""NPU detection and system information module."""

import logging
import platform
from dataclasses import dataclass
from typing import Dict, List, Optional

import psutil

logger = logging.getLogger(__name__)


@dataclass
class NPUInfo:
    """Information about detected NPU hardware."""

    name: str
    device_type: str
    available: bool
    backend: str  # 'openvino', 'onnxruntime', 'directml'
    version: Optional[str] = None
    properties: Optional[Dict] = None

    def __str__(self) -> str:
        status = "Available" if self.available else "Not Available"
        return f"{self.name} ({self.device_type}) - {status} [Backend: {self.backend}]"


class NPUDetector:
    """Detects and provides information about NPU hardware."""

    def __init__(self):
        self.system_info = self._get_system_info()
        self.npu_devices: List[NPUInfo] = []
        self._detect_npus()

    def _get_system_info(self) -> Dict:
        """Get basic system information."""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(logical=False),
            'total_memory': psutil.virtual_memory().total / (1024**3),  # GB
        }

    def _detect_npus(self) -> None:
        """Detect available NPUs using different backends."""
        # Try OpenVINO
        self._detect_openvino_npu()

        # Try ONNX Runtime
        self._detect_onnxruntime_npu()

        if not self.npu_devices:
            logger.warning("No NPU devices detected. Will fallback to CPU.")

    def _detect_openvino_npu(self) -> None:
        """Detect NPUs via OpenVINO."""
        try:
            import openvino as ov

            core = ov.Core()
            available_devices = core.available_devices

            logger.info(f"OpenVINO available devices: {available_devices}")

            for device in available_devices:
                if 'NPU' in device:
                    try:
                        device_name = core.get_property(device, "FULL_DEVICE_NAME")
                        properties = {
                            'full_name': device_name,
                            'supported_properties': core.get_property(device, "SUPPORTED_PROPERTIES"),
                        }

                        npu_info = NPUInfo(
                            name=device_name,
                            device_type=device,
                            available=True,
                            backend='openvino',
                            version=ov.__version__,
                            properties=properties
                        )

                        self.npu_devices.append(npu_info)
                        logger.info(f"Detected OpenVINO NPU: {npu_info}")

                    except Exception as e:
                        logger.warning(f"Error getting info for device {device}: {e}")

        except ImportError:
            logger.info("OpenVINO not available")
        except Exception as e:
            logger.error(f"Error detecting OpenVINO NPUs: {e}")

    def _detect_onnxruntime_npu(self) -> None:
        """Detect NPUs via ONNX Runtime."""
        try:
            import onnxruntime as ort

            providers = ort.get_available_providers()
            logger.info(f"ONNX Runtime available providers: {providers}")

            # Check for NPU-related providers
            npu_providers = [p for p in providers if 'NPU' in p.upper() or 'QNN' in p.upper()]

            for provider in npu_providers:
                npu_info = NPUInfo(
                    name=provider,
                    device_type='NPU',
                    available=True,
                    backend='onnxruntime',
                    version=ort.__version__,
                    properties={'provider': provider}
                )

                # Avoid duplicates
                if not any(npu.name == npu_info.name for npu in self.npu_devices):
                    self.npu_devices.append(npu_info)
                    logger.info(f"Detected ONNX Runtime NPU: {npu_info}")

        except ImportError:
            logger.info("ONNX Runtime not available")
        except Exception as e:
            logger.error(f"Error detecting ONNX Runtime NPUs: {e}")

    def get_best_device(self) -> str:
        """
        Get the best available device for inference.

        Returns:
            Device string (e.g., 'NPU', 'CPU', 'GPU')
        """
        if self.npu_devices:
            # Prefer OpenVINO NPU
            for npu in self.npu_devices:
                if npu.backend == 'openvino' and npu.available:
                    return npu.device_type

            # Otherwise return first available NPU
            return self.npu_devices[0].device_type

        # Fallback to CPU
        logger.warning("No NPU available, using CPU")
        return 'CPU'

    def get_npu_count(self) -> int:
        """Get the number of detected NPUs."""
        return len(self.npu_devices)

    def is_npu_available(self) -> bool:
        """Check if any NPU is available."""
        return len(self.npu_devices) > 0

    def print_device_info(self) -> None:
        """Print detailed information about system and NPU devices."""
        print("\n" + "="*70)
        print("SYSTEM INFORMATION")
        print("="*70)
        for key, value in self.system_info.items():
            print(f"{key:20s}: {value}")

        print("\n" + "="*70)
        print("NPU DEVICES")
        print("="*70)

        if self.npu_devices:
            for i, npu in enumerate(self.npu_devices, 1):
                print(f"\nNPU #{i}:")
                print(f"  Name          : {npu.name}")
                print(f"  Type          : {npu.device_type}")
                print(f"  Backend       : {npu.backend}")
                print(f"  Version       : {npu.version}")
                print(f"  Available     : {npu.available}")
                if npu.properties:
                    print(f"  Properties    : {npu.properties}")
        else:
            print("\nNo NPU devices detected.")
            print("System will use CPU for inference.")

        print("\n" + "="*70)
        print(f"Best device for inference: {self.get_best_device()}")
        print("="*70 + "\n")


def main() -> None:
    """Main function for testing NPU detection."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    detector = NPUDetector()
    detector.print_device_info()


if __name__ == "__main__":
    main()
