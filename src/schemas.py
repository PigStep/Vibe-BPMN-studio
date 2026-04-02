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
