from abc import ABC, abstractmethod
from typing import Literal, Any


# TODO: deprecated. Dead code. Delete
class LLMClient(ABC):
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
