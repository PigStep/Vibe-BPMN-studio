from typing import Callable
from pydantic import Json
from google.genai import types
from src.ai_generation.managers.tool.manager_base import ToolManager
from langchain_google_genai._function_utils import (
    convert_to_genai_function_declarations,
)
from src.ai_generation.llm_clients.gemini import GeminiClient


class GemimiToolManager(ToolManager):
    def __init__(self):
        self.tool_map: dict[str, Callable] = None
        self.function_map: list[Json] = None

    def _create_function_mapping(self, functions: list[Callable]):
        tool_map = {}
        for function in functions:
            tool_map[function.__name__] = function
        self.tool_map = tool_map

    def save_tools(self, tools: list[Callable]):
        self.tools = convert_to_genai_function_declarations(tools)
        return self.tools

    def get_tools(self):
        return self.tools

    def get_function_map(self):
        return self.function_map

    def call_tools(self, llm_client: GeminiClient, prompt: str, **config):
        config = types.GenerateContentConfig(tools=self.tools)
        response = llm_client.generate_response(prompt, config)

        # Check for a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_call.name
            function_call.args

            # call function
            function_to_call = self.function_map[function_call.name]
            result = function_to_call(**function_call.args)
        else:
            print("No function call found in the response.")
            print(response.text)


# Configure the client and tools
# client = genai.Client()
# tools = types.Tool(function_declarations=[schedule_meeting_function])
# config = types.GenerateContentConfig(tools=[tools])

# # Send request with function declarations
# response = client.models.generate_content(
#     model="gemini-3-flash-preview",
#     contents="Schedule a meeting with Bob and Alice for 03/14/2025 at 10:00 AM about the Q3 planning.",
#     config=config,
# )

# # Check for a function call
# if response.candidates[0].content.parts[0].function_call:
#     function_call = response.candidates[0].content.parts[0].function_call
#     print(f"Function to call: {function_call.name}")
#     print(f"ID: {function_call.id}")
#     print(f"Arguments: {function_call.args}")
#     #  In a real app, you would call your function here:
#     #  result = schedule_meeting(**function_call.args)
# else:
#     print("No function call found in the response.")
#     print(response.text)
