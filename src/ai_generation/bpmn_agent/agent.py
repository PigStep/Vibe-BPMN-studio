import logging
from functools import partial

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import (
    InMemorySaver,
)
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from src.ai_generation.bpmn_agent.langgraph import get_langgraph_llm_client
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.state import AgentState
from src.ai_generation.bpmn_agent.nodes import (
    generate_xml,
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
        generate_xml,
        llm=llm,
        configuration=prompt_manager.get_call_config("XML_generation"),
    )

    # Build workflow
    agent_builder.add_node("imagine", generate_process_with_config)
    agent_builder.add_node("generate", generate_bpmn_with_config)

    agent_builder.add_edge(START, "imagine")
    agent_builder.add_edge("imagine", "generate")
    agent_builder.add_edge("generate", "imagine")
    return agent_builder


_checkpointer: BaseCheckpointSaver | None = None


def _get_checkpointer() -> BaseCheckpointSaver:
    global _checkpointer
    if not _checkpointer:
        # TODO: implement fabric to get different checkpointers
        _checkpointer = InMemorySaver()
    return _checkpointer


def get_agent() -> tuple[CompiledStateGraph, BaseCheckpointSaver]:
    checkpointer = _get_checkpointer()
    agent = build_bpmn_agent().compile(checkpointer=checkpointer)
    return agent, checkpointer


def _session_exist(
    checkpointer: BaseCheckpointSaver,
    config: RunnableConfig,
    user_input: SUserInputData,
) -> bool:
    session_exists = checkpointer.get_tuple(config) is not None
    logger.debug(
        "%s, Entering graph. Is first input: %s",
        user_input.session_id,
        not session_exists,
    )
    return session_exists


async def _invoke_agent(
    agent: CompiledStateGraph,
    session_exist: bool,
    config: RunnableConfig,
    user_request: SUserInputData,
) -> dict:
    if session_exist:
        response = await agent.ainvoke(Command(resume=user_request.user_input), config)
    else:
        initial_state = {
            "messages": [HumanMessage(content=user_request.user_input)],
            "session_id": user_request.session_id,
        }
        response = await agent.ainvoke(initial_state, config=config)
    return response


def _proceed_response(response: dict) -> str:
    result = None
    if "__interrupt__" in response:
        logger.debug(
            "Agent was interupted. Interrupt message: %s", response["__interrupt__"]
        )
        # '__interrupt__': [
        # Interrupt(value={"xml_result": "xml code here"}, id='...'),
        # if multiple interrupts called they will be there
        # ]
        result = response["__interrupt__"][0].value["xml_result"]
    else:
        # LLM have not interrupted
        result = response["messages"][-1].content[0]["text"]
    logger.debug("Last agent message: %s", result)
    return result


async def invoke_agent(user_request: SUserInputData) -> str:
    config: RunnableConfig = {"configurable": {"thread_id": user_request.session_id}}
    agent, checkpointer = get_agent()
    # If session exists - continue it
    session_exist = _session_exist(checkpointer, config, user_request)
    response = await _invoke_agent(agent, session_exist, config, user_request)

    return _proceed_response(response)
