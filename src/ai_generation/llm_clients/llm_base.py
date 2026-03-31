from abc import ABC, abstractmethod
from typing import Literal, Any
from src.ai_generation.managers.tool.manager_base import ToolManager


class LLMClient(ABC):
    tool_manager: ToolManager | None = None

    @abstractmethod
    def generate_response_text_based(
        self,
        prompt: str,
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str | None: ...

    @abstractmethod
    def generate_response_json_based(
        self,
        prompt: str,
        json_schema: dict | type[Any],
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str | None: ...

    @abstractmethod
    def generate_response_with_tools(
        self,
        prompt: str,
        system_prompt: str,
        tools: list[Any] | None = None,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> Any: ...
