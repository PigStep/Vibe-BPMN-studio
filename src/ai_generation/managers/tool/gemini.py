from typing import Callable
from pydantic import Json
from src.ai_generation.managers.tool.manager_base import ToolManager
from langchain_google_genai._function_utils import (
    convert_to_genai_function_declarations,
)


class GemimiToolManager(ToolManager):
    def __init__(self):
        self.functions: list[Json] = None

    def save_tools(self, tools: list[Callable]):
        self.tools = convert_to_genai_function_declarations(tools)
        return self.tools

    def get_tools(self):
        return self.tools
