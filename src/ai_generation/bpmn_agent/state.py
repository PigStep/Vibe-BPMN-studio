from langchain_core.messages import BaseMessage
from typing_extensions import Annotated, TypedDict
import operator


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
