from typing import Callable, Any
from langchain_core.utils.function_calling import convert_to_openai_function
from src.ai_generation.managers.tool.manager_base import ToolManager


class OpenAIToolManager(ToolManager):
    def __init__(self):
        self.tools: list[dict[str, Any]] = []
        self.tool_map: dict[str, Callable] = {}

    def save_tools(self, tools: list[Callable]) -> None:
        self.tool_map = {tool.__name__: tool for tool in tools}
        self.tools = [convert_to_openai_function(tool) for tool in tools]

    def get_tools(self) -> list[dict[str, Any]]:
        return self.tools

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name not in self.tool_map:
            raise ValueError(f"Tool '{tool_name}' not found")
        tool = self.tool_map[tool_name]
        result = tool(**arguments)
        return str(result) if result is not None else ""

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self.tool_map
