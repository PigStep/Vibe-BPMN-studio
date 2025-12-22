from typing import Literal
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

    def generate_response(
        self,
        prompt: str,
        response_format: dict | None = None,
        extra_body: dict | None = None,
    ) -> str | None:
        """
        Generate a response from the LLM using the provided prompt.

        Parameters
        ----------
        prompt : str
            The user prompt to send to the model.
        response_format : dict | None, optional
            The format for the model's response
            ```{
            "type": "json_schema",
            "json_schema": {
                "name": "response_schema",
                "schema": json_schema,
            }
            ```

        extra_body : dict | None, optional
            Additional key/value pairs to include in the request body (e.g reasoning effort)
            ```
            extra_body={"reasoning": {"effort": reasoning_mode}}
            ```
        Returns
        -------
        str | None
            The content of the first message in the model's response, or None if no content is returned.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.behaivour_promt},
                {"role": "user", "content": prompt},
            ],
            response_format=response_format if response_format else None,
            extra_body=extra_body if extra_body else None,
        )
        return response.choices[0].message.content

    def generate_response_json_based(
        self,
        prompt: str,
        json_schema: dict,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
    ) -> str | None:
        """
        Generates a JSON-formatted response from the LLM based on the provided prompt and schema.

        Parameters
        ----------
        prompt : str
            The user prompt to be sent to the model.
        json_schema : dict
            A JSON Schema dict that defines the expected structure of the model's output.
        reasoning_mode : Literal["none", "minimal", "low", "medium", "high"], optional
            The level of reasoning effort the model should apply when generating the response.
            Defaults to "none".

        Returns
        -------
        str | None
            The JSON response as a string if the model returns a valid response; otherwise, None.
        """
        return self.generate_response(
            prompt,
            {
                "type": "json_schema",
                "json_schema": {
                    "name": "response_schema",
                    "schema": json_schema,
                },
            },
            extra_body={"reasoning": {"effort": reasoning_mode}},
        )

    def generate_response_text_based(
        self,
        prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
    ) -> str:
        """
        Generates a text-formatted response from the LLM based on the provided prompt.
        Offer a choice of reasoning effort levels.
        """
        return self.generate_response(
            prompt, extra_body={"reasoning": {"effort": reasoning_mode}}
        )
