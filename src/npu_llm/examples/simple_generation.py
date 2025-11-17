#!/usr/bin/env python3
"""
Example: Simple text generation with NPU.

This script demonstrates how to generate text using a pre-loaded LLM model on NPU.
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from npu_llm.models.model_loader import ModelLoader
from npu_llm.models.llm_pipeline import LLMPipeline
from npu_llm.utils.logger import setup_logger


def main():
    """Run text generation example."""
    parser = argparse.ArgumentParser(description="Simple text generation with NPU")
    parser.add_argument(
        "--model-id",
        type=str,
        default="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        help="HuggingFace model ID or local path"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Hello, how are you?",
        help="Text prompt for generation"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=100,
        help="Maximum length of generated text"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="NPU",
        help="Device to use (NPU, CPU, GPU)"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="openvino",
        choices=["openvino", "onnxruntime"],
        help="Backend to use"
    )
    parser.add_argument(
        "--load-local",
        action="store_true",
        help="Load from local path instead of HuggingFace"
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logger()

    try:
        # Load or convert model
        if args.load_local:
            logger.info(f"Loading local model from {args.model_id}")
            model_path = Path(args.model_id)
        else:
            logger.info(f"Loading model {args.model_id} from HuggingFace Hub")
            loader = ModelLoader()
            model_path = loader.load_huggingface_model(
                args.model_id,
                export_format=args.backend
            )

        # Create pipeline
        logger.info(f"Creating LLM pipeline with device={args.device}, backend={args.backend}")
        pipeline = LLMPipeline(
            model_path=model_path,
            device=args.device,
            backend=args.backend
        )

        # Generate text
        logger.info(f"Generating text for prompt: '{args.prompt}'")
        print("\n" + "="*70)
        print("PROMPT:")
        print("="*70)
        print(args.prompt)
        print("\n" + "="*70)
        print("GENERATED TEXT:")
        print("="*70)

        response = pipeline.generate(
            prompt=args.prompt,
            max_length=args.max_length,
            temperature=args.temperature
        )

        print(response)
        print("="*70 + "\n")

        # Optional: Run benchmark
        logger.info("Running performance benchmark...")
        metrics = pipeline.benchmark(args.prompt, iterations=5)

        print("="*70)
        print("PERFORMANCE METRICS:")
        print("="*70)
        print(f"Mean Latency    : {metrics['mean_latency']:.3f}s")
        print(f"Min Latency     : {metrics['min_latency']:.3f}s")
        print(f"Max Latency     : {metrics['max_latency']:.3f}s")
        print(f"Tokens/Second   : {metrics['tokens_per_second']:.2f}")
        print("="*70 + "\n")

    except Exception as e:
        logger.error(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
