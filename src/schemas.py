from pydantic import BaseModel


class SExampleBPMN(BaseModel):
    status: bool = True
    xml: str


class SUserInputData(BaseModel):
    session_id: str
    user_input: str


class SAgentOutput(BaseModel):
    status: bool = True
    output: str


class SToolCall(BaseModel):
    name: str
    arguments: dict


class SLLMResponse(BaseModel):
    text: str | None = None
    tool_calls: list[SToolCall] | None = None
    finish_reason: str | None = None
