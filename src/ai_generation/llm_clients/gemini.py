from typing import Literal
import logging
from google.genai import types
from google import genai
from src.ai_generation.llm_clients.llm_base import LLMClient
from settings import settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class GeminiClient(LLMClient):
    def __init__(self):
        self._setup_client()

    def _setup_client(self):
        self.model_name = settings.GEMINI_MODEL_NAME
        api_key = settings.GEMINI_API_KEY
        logger.debug("Using Gemini API key: %s...", api_key[:10])
        self.client = genai.Client(api_key=api_key)

    def _generate_response(
        self,
        prompt: str,
        generation_config: types.GenerateContentConfig,
    ):
        response = self.client.models.generate_content(
            model=self.model_name,
            config=generation_config,
            contents=prompt,
        )
        return response.text

    def generate_response_text_based(
        self,
        prompt: str,
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str | None:
        return self._generate_response(
            prompt,
            generation_config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                thinking_config=types.ThinkingConfig(thinking_level=reasoning_mode),
            ),
        )

    def generate_response_json_based(
        self,
        prompt: str,
        json_schema: dict | type[BaseModel],
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str | None:
        schema = (
            json_schema.model_json_schema()
            if isinstance(json_schema, type) and issubclass(json_schema, BaseModel)
            else json_schema
        )
        return self._generate_response(
            prompt,
            generation_config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                thinking_config=types.ThinkingConfig(thinking_level=reasoning_mode),
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )


# https://ai.google.dev/api/generate-content?hl=ru#v1beta.GenerationConfig
