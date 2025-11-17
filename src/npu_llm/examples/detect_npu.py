#!/usr/bin/env python3
"""
Example: Detect NPU devices on the system.

This script demonstrates how to use the NPUDetector to find available NPU hardware.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from npu_llm.core.npu_detector import NPUDetector
from npu_llm.utils.logger import setup_logger


def main():
    """Detect and display NPU information."""
    # Setup logging
    logger = setup_logger()

    logger.info("Starting NPU detection...")

    # Create detector
    detector = NPUDetector()

    # Print detailed information
    detector.print_device_info()

    # Check NPU availability
    if detector.is_npu_available():
        logger.info(f"✓ Found {detector.get_npu_count()} NPU device(s)")
        logger.info(f"Best device for inference: {detector.get_best_device()}")
    else:
        logger.warning("✗ No NPU devices found. System will use CPU.")


if __name__ == "__main__":
    main()
