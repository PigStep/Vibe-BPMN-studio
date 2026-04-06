from langchain_core.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
from functools import partial

from src.ai_generation.llm_clients import get_llm_client, get_langgraph_llm_client
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.state import AgentState
from src.ai_generation.bpmn_agent.nodes import generate_bpmn
from src.ai_generation.bpmn_agent.nodes import generate_process
from src.schemas import SUserInputData


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


_agent = None


def get_agent_answer(initial_state: dict) -> dict:
    global _agent
    if _agent is None:
        _agent = build_bpmn_agent().compile()
    result = _agent.invoke(initial_state)
    return result["messages"][-1].content[0]["text"]


def invoke_agent(user_input: SUserInputData) -> str:
    initial_state = {"messages": [HumanMessage(content=user_input.user_input)]}
    return get_agent_answer(initial_state)
