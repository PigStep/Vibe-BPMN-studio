from typing import Literal
from google.genai import types
from google import genai
from src.ai_generation.llm_clients.llm_base import LLMClient
from settings import settings


class GeminiClient(LLMClient):
    """
    LLM client for Gemini

    Notes:
        The client gets the API key from the environment variable `GEMINI_API_KEY`.
    """

    def __init__(self):
        self.model_name = settings.GEMINI_MODEL_NAME
        # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        self.client = genai.Client()

    def _generate_response(
        self,
        prompt: str,
        system_prompt: str,
        json_schema: dict | None = None,
        reasoning_mode: Literal["minimal", "low", "medium", "high"] | None = "low",
        temperature: float | None = None,
    ):
        response = self.client.models.generate_content(
            model=self.model_name,
            config=types.GenerateContentConfig(
                # Reasoning mode
                thinking_config=types.ThinkingConfig(thinking_level=reasoning_mode),
                # System prompt
                system_instruction=system_prompt,
                # Temperature
                temperature=temperature,
                # Json schema (if needed)
                json_schema=json_schema if json_schema else None,
            ),
            contents=prompt,
        )
        return response.text

    def generate_response_text_based(
        self,
        prompt: str,
        system_prompt: str,
        reasoning_mode: Literal["minimal", "low", "medium", "high"] | None = "low",
        temperature: float | None = None,
    ) -> str:
        return self._generate_response(
            prompt, system_prompt, reasoning_mode, temperature
        )

    def generate_response_json_based(
        self,
        prompt: str,
        system_prompt: str,
        json_schema: dict,
        reasoning_mode: Literal["minimal", "low", "medium", "high"] | None = "low",
        temperature: float | None = None,
    ):
        return self._generate_response(
            prompt, system_prompt, reasoning_mode, temperature, json_schema
        )


# https://ai.google.dev/api/generate-content?hl=ru#v1beta.GenerationConfig
