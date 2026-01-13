from typing_extensions import TypedDict


class SimpleBPMNAgent(TypedDict):
    user_prompt: str
    user_edit_promt: str
    thread_id: str

    xml_content: str
    clean_xml: str | None
    is_valid: bool
    validation_error: str | None

    previous_answer: str
