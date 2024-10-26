# llm_handler.py

import os
from typing import Optional
import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import logging
import tiktoken
import asyncio
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """Data class for standardized LLM response"""

    text: str
    prompt_tokens: int
    completion_tokens: int
    reasoning_tokens: Optional[int] = None


class LLMHandler:
    """Handler for LLM API calls across different providers"""

    def __init__(self):
        """Initialize API clients using environment variables"""
        load_dotenv()

        # Validate API keys
        self._openai_key = os.getenv("OPENAI_API_KEY")
        self._anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self._google_key = os.getenv("GOOGLE_API_KEY")

        if not self._openai_key:
            logger.warning("OpenAI API key not found in environment variables")
        if not self._anthropic_key:
            logger.warning("Anthropic API key not found in environment variables")
        if not self._google_key:
            logger.warning("Google API key not found in environment variables")

        # Initialize API clients
        if self._openai_key:
            self.openai_client = openai.AsyncOpenAI(api_key=self._openai_key)
        if self._anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self._anthropic_key)
        if self._google_key:
            genai.configure(api_key=self._google_key)
            self.gemini_model = genai.GenerativeModel("gemini-1.5-pro")

        # Define supported models with specifications
        self.SUPPORTED_MODELS = {
            # OpenAI Models
            "gpt-4-0125-preview": {
                "provider": "openai",
                "context_window": 128000,
                "max_output_tokens": 16384,
                "series": "gpt",
            },
            "gpt-4-turbo-preview": {
                "provider": "openai",
                "context_window": 128000,
                "max_output_tokens": 16384,
                "series": "gpt",
            },
            "o1-preview-2024-09-12": {
                "provider": "openai",
                "context_window": 128000,
                "max_output_tokens": 32768,
                "series": "o1",
            },
            "o1-mini-2024-09-12": {
                "provider": "openai",
                "context_window": 128000,
                "max_output_tokens": 65536,
                "series": "o1",
            },
            # Anthropic Models
            "claude-3-opus-20240229": {
                "provider": "anthropic",
                "context_window": 200000,
                "max_output_tokens": 4096,
            },
            "claude-3-sonnet-20240229": {
                "provider": "anthropic",
                "context_window": 200000,
                "max_output_tokens": 8192,
            },
            # Google Models
            "gemini-1.5-pro": {
                "provider": "google",
                "context_window": 2097152,  # ~2M tokens
                "max_output_tokens": 8192,
            },
        }

    def _validate_token_limits(
        self, model: str, prompt: str, max_tokens: Optional[int]
    ):
        """Validate token limits for the given model and prompt"""
        model_specs = self.SUPPORTED_MODELS[model]

        # Get tokenizer based on provider
        tokenizer = tiktoken.encoding_for_model(
            "gpt-4"
        )  # Use GPT-4 tokenizer as approximation

        prompt_tokens = len(tokenizer.encode(prompt))
        max_output = max_tokens or model_specs["max_output_tokens"]

        if prompt_tokens > model_specs["context_window"]:
            raise ValueError(
                f"Prompt length ({prompt_tokens} tokens) exceeds model's context window "
                f"({model_specs['context_window']} tokens)"
            )

        if max_output > model_specs["max_output_tokens"]:
            raise ValueError(
                f"Requested max_tokens ({max_output}) exceeds model's maximum output tokens "
                f"({model_specs['max_output_tokens']})"
            )

    async def get_completion(
        self,
        prompt: str,
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[str] = None,
    ) -> LLMResponse:
        """
        Get completion from specified LLM model.

        Args:
            prompt: Input text prompt
            model: Model identifier string
            temperature: Optional temperature parameter for response randomness
            max_tokens: Optional maximum tokens for response
            response_format: Optional response format specification

        Returns:
            LLMResponse object containing response text and token counts

        Raises:
            ValueError: If model is not supported or token limits are exceeded
            Exception: For API errors or other issues
        """
        try:
            if model not in self.SUPPORTED_MODELS:
                raise ValueError(
                    f"Unsupported model: {model}. Supported models: {list(self.SUPPORTED_MODELS.keys())}"
                )

            # Validate token limits
            self._validate_token_limits(model, prompt, max_tokens)

            provider = self.SUPPORTED_MODELS[model]["provider"]

            if provider == "openai":
                return await self._handle_openai_completion(
                    prompt, model, temperature, max_tokens, response_format
                )
            elif provider == "anthropic":
                return await self._handle_anthropic_completion(
                    prompt, model, temperature, max_tokens, response_format
                )
            else:  # google
                return await self._handle_gemini_completion(
                    prompt, temperature, max_tokens, response_format
                )

        except Exception as e:
            logger.error(f"Error in get_completion: {e}")
            raise

    async def _handle_openai_completion(
        self,
        prompt: str,
        model: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
        response_format: Optional[str],
    ) -> LLMResponse:
        """Handle OpenAI API completion request"""
        if not self._openai_key:
            raise ValueError("OpenAI API key not found in environment variables")

        try:
            messages = [{"role": "user", "content": prompt}]
            completion_config = {
                "model": model,
                "messages": messages,
            }

            # Handle O1 series specifics
            if model.startswith("o1-"):
                if temperature is not None:
                    logger.warning(
                        f"Temperature parameter is not supported for {model}, ignoring temperature={temperature}"
                    )
                if max_tokens is not None:
                    completion_config["max_completion_tokens"] = max_tokens
            else:
                if temperature is not None:
                    completion_config["temperature"] = temperature
                if max_tokens is not None:
                    completion_config["max_tokens"] = max_tokens

            if response_format:
                completion_config["response_format"] = {"type": response_format}

            response = await self.openai_client.chat.completions.create(
                **completion_config
            )

            return LLMResponse(
                text=response.choices[0].message.content,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
            )

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def _handle_anthropic_completion(
        self,
        prompt: str,
        model: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
        response_format: Optional[str],  # Kept for API consistency
    ) -> LLMResponse:
        """
        Handle Anthropic API completion request

        Note: response_format parameter is ignored as Anthropic API doesn't support format specification
        """
        if not self._anthropic_key:
            raise ValueError("Anthropic API key not found in environment variables")

        if response_format:
            logger.warning(
                f"Response format '{response_format}' is not supported by Anthropic API and will be ignored"
            )

        try:
            completion_config = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }

            if temperature is not None:
                completion_config["temperature"] = temperature
            if max_tokens is not None:
                completion_config["max_tokens"] = max_tokens
            else:
                completion_config["max_tokens"] = 4096

            response = await asyncio.to_thread(
                self.anthropic_client.messages.create, **completion_config
            )

            return LLMResponse(
                text=response.content[0].text,
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
            )

        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise

    async def _handle_gemini_completion(
        self,
        prompt: str,
        temperature: Optional[float],
        max_tokens: Optional[int],
        response_format: Optional[str],  # Kept for API consistency
    ) -> LLMResponse:
        """
        Handle Google Gemini API completion request

        Note: response_format parameter is ignored as Gemini API doesn't support format specification
        """
        if not self._google_key:
            raise ValueError("Google API key not found in environment variables")

        if response_format:
            logger.warning(
                f"Response format '{response_format}' is not supported by Gemini API and will be ignored"
            )

        try:
            generation_config = {}
            if temperature is not None:
                generation_config["temperature"] = temperature
            if max_tokens is not None:
                generation_config["max_output_tokens"] = max_tokens

            response = await self.gemini_model.generate_content_async(
                prompt,
                generation_config=generation_config if generation_config else None,
            )

            # Use tiktoken for consistent token counting
            tokenizer = tiktoken.encoding_for_model("gpt-4")
            prompt_tokens = len(tokenizer.encode(prompt))
            completion_tokens = len(tokenizer.encode(response.text))

            return LLMResponse(
                text=response.text,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise

    def get_completion_sync(
        self,
        prompt: str,
        model: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[str] = None,
    ) -> LLMResponse:
        """
        Synchronous wrapper for get_completion
        """
        return asyncio.run(
            self.get_completion(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format,
            )
        )
