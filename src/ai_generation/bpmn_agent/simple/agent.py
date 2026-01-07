from langgraph.graph import START, END, StateGraph
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


def get_agent_answer(initial_state: dict) -> dict:
    global _agent
    if _agent is None:
        _agent = build_bpmn_agent().compile()
    result = _agent.invoke(initial_state)
    return result


def invoke_agent(user_input: SUserInputData) -> str:
    initial_state = {
        "user_input": user_input.user_input,
        "previous_stage": "",
    }
    return get_agent_answer(initial_state)
