import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from langgraph.graph import START, END, StateGraph
from functools import partial
from langgraph.checkpoint.memory import (
    InMemorySaver,
    BaseCheckpointSaver,
)
from langgraph.graph.state import CompiledStateGraph

from src.ai_generation.bpmn_agent.langgraph import get_langgraph_llm_client
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.state import AgentState
from src.ai_generation.bpmn_agent.nodes import (
    generate_bpmn,
    generate_process,
)
from src.schemas import SUserInputData

logger = logging.getLogger(__name__)


def build_bpmn_agent() -> StateGraph:
    # Define managers and LLM client
    llm = get_langgraph_llm_client()
    prompt_manager = LLMConfigManager(r"data/prompts/")
    agent_builder = StateGraph(AgentState)

    # Define node with partial
    generate_process_with_config = partial(
        generate_process,
        llm=llm,
        configuration=prompt_manager.get_call_config("business_generation"),
    )
    generate_bpmn_with_config = partial(
        generate_bpmn,
        llm=llm,
        configuration=prompt_manager.get_call_config("XML_generation"),
    )

    # Build workflow
    agent_builder.add_node("imagine", generate_process_with_config)
    agent_builder.add_node("generate", generate_bpmn_with_config)

    agent_builder.add_edge(START, "imagine")
    agent_builder.add_edge("imagine", "generate")
    agent_builder.add_edge("generate", END)
    return agent_builder


_checkpointer: BaseCheckpointSaver | None = None
_agent: BaseChatModel | None = None


def get_agent():
    global _agent, _checkpointer
    if _agent is None:
        # TODO: implement fabric to get different checkpointers
        _checkpointer = InMemorySaver()
        _agent = build_bpmn_agent().compile(checkpointer=_checkpointer)
    return _agent, _checkpointer


def _get_user_data(
    checkpointer: BaseCheckpointSaver,
    initial_state: dict,
    config: RunnableConfig,
    user_input: SUserInputData,
):
    session_exists = checkpointer.get_tuple(config) is not None
    logger.debug("%s, Entering graph. Is first input: %s", not session_exists)
    # Resume graph if user had conversation before, initial state if this is first invoke
    input_data = (
        Command(goto="imagine", resume=user_input.user_input)  # Load user feedback
        if session_exists
        else initial_state
    )
    return input_data


def get_agent_answer(
    agent: CompiledStateGraph, invoke_data: dict, config: RunnableConfig
) -> dict:
    result = agent.invoke(invoke_data, config=config)
    return result["messages"][-1].content[0]["text"]


def invoke_agent(user_input: SUserInputData) -> str:
    initial_state = {"messages": [HumanMessage(content=user_input.user_input)]}
    config: RunnableConfig = {"configurable": {"thread_id": user_input.session_id}}
    agent, checkpointer = get_agent()
    invoke_data = _get_user_data(checkpointer, initial_state, config, user_input)

    return get_agent_answer(agent, invoke_data, config)
