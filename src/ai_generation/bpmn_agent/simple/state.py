from typing_extensions import TypedDict


class SimpleBPMNAgent(TypedDict):
    user_input: str
    previous_answer: str
    user_edit_promt: str
