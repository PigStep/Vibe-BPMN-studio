from typing import Literal
from langgraph.graph import StateGraph, START, END
from functools import partial
import logging

from ai_generation.managers.llm_config import get_basic_llm_config_manager
from src.ai_generation.managers.json_schema import get_json_schema_namager
from src.ai_generation.bpmn_agent.state import BPMNState, getBpmnClient
from src.ai_generation.bpmn_agent.simple.get_bpmn_node import generate_bpmn
from src.ai_generation.bpmn_agent.simple.imagine_procces_node import generate_process

config_manager = get_basic_llm_config_manager()
schema_manager = get_json_schema_namager()
llm = getBpmnClient()

logger = logging.getLogger(__name__)

generate_xml = partial(
    generate_bpmn,
    llm=llm,
    configuration=config_manager.get_call_config("XML_generation"),
)
imagine_process = partial(
    generate_process,
    llm=llm,
    configuration=config_manager.get_call_config("business_generation"),
)


def all_steps_done(state: BPMNState) -> Literal["true", "false"]:
    plan_dict = state["plan"]
    if len(plan_dict) - 1 == state["execution_step"]:
        return "true"
    logger.info(
        "Plan is not done. Current step: %s from plan length: %s",
        state["execution_step"],
        len(plan_dict) - 1,
    )
    return "false"


# Build workflow
agent_builder = StateGraph(BPMNState)

# Add nodes
agent_builder.add_node("plan", generate_xml)
agent_builder.add_node("execute", imagine_process)

# Define edges
agent_builder.add_edge(START, "plan")
agent_builder.add_edge("plan", "execute")
agent_builder.add_conditional_edges(
    "execute", all_steps_done, {"true": END, "false": "execute"}
)
# Compile the agent
agent = agent_builder.compile()


def get_agent():
    return agent
