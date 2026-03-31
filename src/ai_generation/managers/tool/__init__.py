from typing import Literal
from src.ai_generation.managers.tool.gemini import GeminiToolManager
from src.ai_generation.managers.tool.openrouter import OpenAIToolManager
from src.ai_generation.managers.tool.manager_base import ToolManager

_manager: ToolManager | None = None


def get_tool_manager(provider: Literal["openrouter", "gemini"]) -> ToolManager:
    global _manager
    if _manager is None:
        match provider:
            case "gemini":
                _manager = GeminiToolManager()
            case "openrouter":
                _manager = OpenAIToolManager()
            case _:
                raise ValueError(f"Unknown provider: {provider}")
    return _manager


def reset_tool_manager():
    global _manager
    _manager = None
