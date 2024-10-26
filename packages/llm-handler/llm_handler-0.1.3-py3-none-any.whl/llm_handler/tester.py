import asyncio
from llm_handler import LLMHandler
import logging

# test_llm_handler.py

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_all_models():
    handler = LLMHandler()

    # Test prompts of varying complexity
    prompts = {
        "simple": "What is 2+2?",
    }

    # Test configurations - separate for O1 and non-O1 models
    regular_configs = [
        {"temperature": 0.7, "max_tokens": 100},
        {"temperature": 1.0, "max_tokens": None},
    ]

    o1_configs = [
        {"max_tokens": 100},
        {"max_tokens": None},
    ]

    for model in handler.SUPPORTED_MODELS.keys():
        logger.info(f"\n=== Testing {model} ===")

        # Choose appropriate configs based on model type
        configs = o1_configs if model.startswith("o1-") else regular_configs

        for prompt_type, prompt in prompts.items():
            logger.info(f"\nTesting {prompt_type} prompt:")

            for config in configs:
                try:
                    logger.info(f"Config: {config}")

                    response = await handler.get_completion(
                        prompt=prompt, model=model, **config
                    )

                    logger.info(f"Success!")
                    logger.info(f"Prompt tokens: {response.prompt_tokens}")
                    logger.info(f"Completion tokens: {response.completion_tokens}")
                    logger.info(
                        f"First 100 chars of response: {response.text[:100]}..."
                    )

                except Exception as e:
                    logger.error(f"Error with {model} using config {config}: {str(e)}")


asyncio.run(test_all_models())
