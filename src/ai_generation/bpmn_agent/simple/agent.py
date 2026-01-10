from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from functools import partial

from src.ai_generation.llm_client import get_llm_client
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.simple.state import SimpleBPMNAgent
from src.ai_generation.bpmn_agent.simple.get_bpmn_node import generate_bpmn
from src.schemas import SUserInputData
from src.ai_generation.bpmn_agent.simple.imagine_procces_node import generate_process


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

    agent_builder.add_edge(START, "imagine")
    agent_builder.add_edge("imagine", "generate")
    agent_builder.add_edge("generate", END)

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
    initial_state = {
        "user_input": user_input.user_input,
        "previous_stage": "",
    }
    return agent.invoke(initial_state, config=config)


def invoke_agent(user_input: SUserInputData, thread_id: str) -> str:
    """Invoke agent with curtrent sssion (thread_id)"""
    return get_agent_answer(user_input, thread_id)
