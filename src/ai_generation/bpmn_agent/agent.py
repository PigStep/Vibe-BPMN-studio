from typing import Literal
from langgraph.graph import StateGraph, START, END
from functools import partial
from src.ai_generation.managers.promt import get_prompt_manager
from src.ai_generation.managers.json_schema import get_json_schema_namager
from .state import BPMNState, getBpmnClient
from .nodes.plan import plan
from .nodes.execution import execute

promt_manager = get_prompt_manager()
schema_manager = get_json_schema_namager()
llm = getBpmnClient()


plan_with_config = partial(
    plan, prompt_manager=promt_manager, llm=llm, schema_manager=schema_manager
)
execute_with_config = partial(
    execute, prompt_manager=promt_manager, llm=llm, schema_manager=schema_manager
)


def all_steps_done(state: BPMNState) -> Literal["true", "false"]:
    plan_dict = state["plan"]
    if len(plan_dict) - 1 == len(state["execution_step"]):
        return "true"
    return "false"


# Build workflow
agent_builder = StateGraph(BPMNState)

# Add nodes
agent_builder.add_node("plan", plan_with_config)
agent_builder.add_node("execute", execute_with_config)

# Define edges
agent_builder.add_edge(START, "plan")
agent_builder.add_conditional_edges(
    "plan", all_steps_done, {"true": END, "false": "execute"}
)

# Compile the agent
agent = agent_builder.compile()


def get_agent():
    return agent
