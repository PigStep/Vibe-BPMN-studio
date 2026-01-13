from typing_extensions import Literal
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from functools import partial

from src.ai_generation.llm_client import get_llm_client
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.simple.state import SimpleBPMNAgent
from src.schemas import SUserInputData

from src.ai_generation.bpmn_agent.simple.nodes.get_bpmn import generate_bpmn
from src.ai_generation.bpmn_agent.simple.nodes.validate_xml import validate_xml
from src.ai_generation.bpmn_agent.simple.nodes.imagine_procces import generate_process
from src.ai_generation.bpmn_agent.simple.nodes.wait_refactor import wait_refactor


def check_validation(state: SimpleBPMNAgent) -> Literal["true", "false"]:
    return "true" if state.get("is_valid", False) else "false"


def build_bpmn_agent() -> StateGraph:
    # Define managers and LLM client
    llm = get_llm_client()
    prompt_manager = LLMConfigManager(r"data/prompts/simple")
    agent_builder = StateGraph(SimpleBPMNAgent)

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
    agent_builder.add_node("validate", validate_xml)
    agent_builder.add_node("refactor", ...)  # TODO: add refactor node
    agent_builder.add_node("wait", wait_refactor)

    agent_builder.add_edge(START, "imagine")
    agent_builder.add_edge("imagine", "generate")
    agent_builder.add_edge("generate", "wait")
    agent_builder.add_edge("wait", "validate")

    agent_builder.add_conditional_edges(
        "validate", check_validation, {"true": "wait", "false": "refactor"}
    )

    return agent_builder


_agent = None


def _reset_agent() -> bool:
    global _agent_agent
    _agent = None
    return True


def get_compiled_agent():
    """Lazy initialization of agent with memory"""
    global _agent
    if _agent is None:
        # creating checkpoint saver
        memory = InMemorySaver()
        _agent = build_bpmn_agent().compile(checkpointer=memory)
    return _agent


def get_agent_answer(user_input: SUserInputData, thread_id: str) -> dict:
    agent = get_compiled_agent()

    # Setting up agent
    config = {"configurable": {"thread_id": thread_id}}

    # Check was agent waiting editing
    agent_previous_state = agent.get_state({"configurable": {"thread_id": thread_id}})
    if agent_previous_state:
        # If memory is active, our agent should be resumed
        return agent.invoke(Command(resume=user_input))
    initial_state = {
        "user_input": user_input.user_input,
        "thread_id": thread_id,
        "previous_stage": "",
    }
    return agent.invoke(initial_state, config=config)


def invoke_agent(user_input: SUserInputData, thread_id: str) -> str:
    """Invoke agent with curtrent sssion (thread_id)"""
    return get_agent_answer(user_input, thread_id)
