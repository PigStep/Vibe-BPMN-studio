from typing import Callable, Any
import logging
from langchain_google_genai._function_utils import (
    convert_to_genai_function_declarations,
)
from src.ai_generation.managers.tool.manager_base import ToolManager

logger = logging.getLogger(__name__)


class GeminiToolManager(ToolManager):
    def __init__(self):
        self.tools: list[Any] = []
        self.tool_map: dict[str, Callable] = {}

    def save_tools(self, tools: list[Callable]) -> None:
        self.tool_map = {tool.__name__: tool for tool in tools}
        genai_tools = convert_to_genai_function_declarations(tools)
        self.tools = genai_tools

    def get_tools(self) -> list[Any]:
        return self.tools

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name not in self.tool_map:
            raise ValueError(f"Tool '{tool_name}' not found")
        tool = self.tool_map[tool_name]
        result = tool(**arguments)
        return str(result) if result is not None else ""

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self.tool_map
