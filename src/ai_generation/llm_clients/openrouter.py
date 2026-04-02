from typing import Literal, Any
from openai import OpenAI
from settings import get_settings
from src.ai_generation.llm_clients.llm_base import LLMClient, SToolCall
from pydantic import BaseModel


# TODO: deprecated. Will be removed in future
class OpenRouterClient(LLMClient):
    def __init__(self):
        self._setup_client()

    def _setup_client(self):
        settings = get_settings()
        AI_API_KEY = settings.OPENROUTER_API_KEY
        self.model_name = settings.OPENROUTER_MODEL_NAME
        self.client = OpenAI(
            api_key=AI_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def _generate_response(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float | None = None,
        response_format: dict | None = None,
        extra_body: dict | None = None,
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str | None = None,
    ) -> Any:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            response_format=response_format if response_format else None,
            extra_body=extra_body if extra_body else None,
            tools=tools,
            tool_choice=tool_choice if tool_choice else None,
        )
        return response

    def generate_response_json_based(
        self,
        prompt: str,
        json_schema: dict | type["BaseModel"],
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str | None:
        schema = (
            json_schema.model_json_schema()
            if isinstance(json_schema, type) and issubclass(json_schema, BaseModel)
            else json_schema
        )
        response = self._generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response_schema",
                    "schema": schema,
                },
            },
            extra_body={"reasoning": {"effort": reasoning_mode}},
            temperature=temperature,
        )
        return response.choices[0].message.content

    def generate_response_text_based(
        self,
        prompt: str,
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str | None:
        response = self._generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            extra_body={"reasoning": {"effort": reasoning_mode}},
            temperature=temperature,
        )
        return response.choices[0].message.content
