from openai import OpenAI
from settings import get_settings

settings = get_settings()

AI_API_KEY = settings.OPENROUTER_API_KEY
MODEL_NAME = settings.OPENROUTER_MODEL_NAME


class LLMClient:
    def __init__(self, client: OpenAI, model_name: str, behaivour_promt: str):
        self.client = client
        self.model_name = model_name
        self.behaivour_promt = behaivour_promt

    def generate_response_json_based(self, prompt: str, json_schema: dict) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.behaivour_promt},
                {"role": "user", "content": prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response_schema",
                    "schema": json_schema,
                },
            },
        )
        return response.choices[0].message.content

    def generate_response_text_based(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.behaivour_promt},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
