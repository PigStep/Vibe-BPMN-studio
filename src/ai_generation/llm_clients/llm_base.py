from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate_response_text_based() -> str: ...

    @abstractmethod
    def generate_response_json_based() -> str: ...
