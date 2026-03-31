from abc import ABC, abstractmethod
from typing import Callable
from pydantic import Json


class ToolManager(ABC):
    """
    Return function call JSON object for choosen aggregator (Gemini, OpenAI)
    """

    @abstractmethod
    def save_tools(self, tools: list[Callable]): ...

    @abstractmethod
    def get_tools(self) -> list[Json]: ...
