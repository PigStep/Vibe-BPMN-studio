from abc import ABC, abstractmethod
from typing import Callable
from pydantic import Json
from src.ai_generation.llm_clients.llm_base import LLMClient


class ToolManager(ABC):
    """
    Return function call JSON object for choosen aggregator (Gemini, OpenAI)
    """

    @abstractmethod
    def save_tools(self, tools: list[Callable]): ...

    @abstractmethod
    def get_tools(self) -> list[Json]: ...

    @abstractmethod
    def call_tools(self, llm_client: LLMClient, prompt: str, **config) -> str: ...
