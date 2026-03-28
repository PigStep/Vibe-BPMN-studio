from pydantic import BaseModel


class SExampleBPMN(BaseModel):
    status: bool = True
    xml: str


# TODO: update class add session ID
class SUserInputData(BaseModel):
    user_input: str


class SAgentOutput(BaseModel):
    status: bool = True
    output: str
