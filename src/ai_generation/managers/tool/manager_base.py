from abc import ABC, abstractmethod
from typing import Any
from langchain_core.tools.structured import StructuredTool
from pydantic import BaseModel


class SToolCall(BaseModel):
    name: str
    arguments: dict


class ToolManager(ABC):
    @abstractmethod
    def save_tools(self, tools: list[StructuredTool]) -> None:
        """Convert and store tools in provider-specific format."""

    @abstractmethod
    def get_tools(self) -> list[Any]:
        """Return tools formatted for LLM request."""

    @abstractmethod
    def execute_tool(self, tool: SToolCall) -> str:
        """Execute a tool by name with given arguments."""

    @abstractmethod
    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool with given name exists."""
