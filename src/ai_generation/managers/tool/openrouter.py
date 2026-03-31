from typing import Callable
from pydantic import Json
from langchain_core.utils.function_calling import convert_to_openai_function
from src.ai_generation.managers.tool.manager_base import ToolManager


class OpenAIToolManager(ToolManager):
    def __init__(self):
        self.tools: list[Json] = None

    def save_tools(self, tools: list[Callable]):
        new_tools = []
        for tool in tools:
            new_tools.append(convert_to_openai_function(tool))
        self.tools = new_tools
        return self.tools

    def get_tools(self):
        return self.tools
