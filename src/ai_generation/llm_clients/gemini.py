from typing import Literal
import logging
from google.genai import types
from google import genai
from pydantic import BaseModel
from langchain_core.tools.structured import StructuredTool
from src.ai_generation.llm_clients.llm_base import LLMClient, SToolCall
from src.ai_generation.managers.tool.gemini import GeminiToolManager
from settings import settings

logger = logging.getLogger(__name__)


class GeminiClient(LLMClient):
    def __init__(self):
        self.tool_manager: GeminiToolManager | None = None
        self._setup_client()

    def _setup_client(self):
        self.model_name = settings.GEMINI_MODEL_NAME
        api_key = settings.GEMINI_API_KEY
        logger.debug("Using Gemini API key: %s...", api_key[:10])
        self.client = genai.Client(api_key=api_key)
        self.tool_manager = GeminiToolManager()

    def generate_response(
        self,
        prompt: str,
        generation_config: types.GenerateContentConfig,
    ) -> str | None:
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
        return self.generate_response(
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
        return self.generate_response(
            prompt,
            generation_config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=temperature,
                thinking_config=types.ThinkingConfig(thinking_level=reasoning_mode),
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )

    def _proceed_response(self, response) -> SToolCall:
        """
        Assemble LLM tool output to class
        """
        tool_calls: list[SToolCall] | None = None

        for part in response.candidates[0].content.parts:
            if part.function_call:
                fc = part.function_call
                if tool_calls is None:
                    tool_calls = []
                tool_calls.append(SToolCall(name=fc.name, arguments=dict(fc.args)))

        return tool_calls

    def generate_tool_call(
        self,
        prompt: str,
        system_prompt: str,
        tools: list[StructuredTool] | None = None,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> list[SToolCall]:
        if tools:
            self.tool_manager.save_tools(tools)
            tools_config = self.tool_manager.get_tools()
        else:
            tools_config = None

        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=temperature,
            thinking_config=types.ThinkingConfig(thinking_level=reasoning_mode),
            tools=tools_config,
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            config=config,
            contents=prompt,
        )

        return self._proceed_response(response)
