#!/usr/bin/env python3
"""
Example: Interactive chat with NPU-accelerated LLM.

This script demonstrates how to create an interactive chat session with an LLM on NPU.
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
    """Run interactive chat demo."""
    parser = argparse.ArgumentParser(description="Interactive chat with NPU")
    parser.add_argument(
        "--model-id",
        type=str,
        default="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        help="HuggingFace model ID or local path"
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

        # Interactive chat loop
        print("\n" + "="*70)
        print("NPU-LLM CHAT DEMO")
        print("="*70)
        print("Type 'quit' or 'exit' to end the conversation")
        print("Type 'clear' to clear chat history")
        print("="*70 + "\n")

        messages = []

        while True:
            # Get user input
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nGoodbye!")
                break

            if not user_input:
                continue

            # Check for special commands
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break

            if user_input.lower() == 'clear':
                messages = []
                print("Chat history cleared.\n")
                continue

            # Add user message
            messages.append({"role": "user", "content": user_input})

            # Generate response
            try:
                response = pipeline.chat(messages, max_length=512, temperature=0.7)

                # Extract only the assistant's response (remove prompt)
                # This is a simple heuristic - may need adjustment based on model
                if "assistant:" in response:
                    response = response.split("assistant:")[-1].strip()

                print(f"Assistant: {response}\n")

                # Add assistant response to history
                messages.append({"role": "assistant", "content": response})

            except Exception as e:
                logger.error(f"Error generating response: {e}")
                print(f"Error: {e}\n")
                # Remove the last user message since generation failed
                messages.pop()

    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
