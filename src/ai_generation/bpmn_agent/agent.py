from settings import settings
from langchain_classic.schema import AIMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from src.ai_generation.llm_clients.llm_base import LLMClient
from src.ai_generation.managers.llm_config import LLMConfigManager
from src.ai_generation.bpmn_agent.tools.generate_bpmn_draft import generate_draft
from src.ai_generation.llm_clients import get_llm_client, get_langgraph_llm_client
from src.schemas import SUserInputData


def get_dependencies() -> tuple[LLMConfigManager, LLMClient, BaseChatModel]:
    config_manager = LLMConfigManager(r"data/prompts/")
    llm = get_langgraph_llm_client()
    non_langgraph_llm = get_llm_client()

    llm_with_tools = llm.bind_tools([generate_draft])

    return (config_manager, non_langgraph_llm, llm_with_tools)


def _run_tools(
    response: AIMessage,
    non_langgraph_llm: LLMClient,
    config_manager: LLMConfigManager,
    session_id: str,
):
    for tool_call in response.tool_calls:
        result = generate_draft.invoke(
            tool_call["args"],
            config={
                "configurable": {
                    "llm": non_langgraph_llm,
                    "config_manager": config_manager,
                    "session_id": session_id,
                }
            },
        )
        # FIXME: 1 tool for now - return first tool
        return result


def get_agent_answer(
    user_input: SUserInputData,
    llm_with_tools: BaseChatModel,
    non_langgraph_llm: LLMClient,
    config_manager: LLMConfigManager,
):
    response = llm_with_tools.invoke([HumanMessage(content=user_input.user_input)])
    return _run_tools(
        response, non_langgraph_llm, config_manager, user_input.session_id
    )


def invoke_agent(user_input: SUserInputData) -> str:
    config_manager, non_langgraph_llm, llm_with_tools = get_dependencies()
    return get_agent_answer(
        user_input,
        llm_with_tools,
        non_langgraph_llm,
        config_manager,
    )
