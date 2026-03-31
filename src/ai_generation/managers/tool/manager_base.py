from abc import ABC, abstractmethod
from typing import Callable, Any
from pydantic import Json


class ToolManager(ABC):
    @abstractmethod
    def save_tools(self, tools: list[Callable]) -> None:
        """Convert and store tools in provider-specific format."""

    @abstractmethod
    def get_tools(self) -> list[Any]:
        """Return tools formatted for LLM request."""

    @abstractmethod
    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool by name with given arguments."""

    @abstractmethod
    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool with given name exists."""
