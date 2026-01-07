from typing import Literal
from openai import OpenAI
from settings import get_settings

settings = get_settings()

AI_API_KEY = settings.OPENROUTER_API_KEY
MODEL_NAME = settings.OPENROUTER_MODEL_NAME


class LLMClient:
    def __init__(self, client: OpenAI, model_name: str):
        self.client = client
        self.model_name = model_name

    def _generate_response(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float = 0.7,
        response_format: dict | None = None,
        extra_body: dict | None = None,
    ) -> str | None:
        """
        Generate a response from the LLM using the provided prompt.

        Parameters
        ----------
        prompt : str
            The user prompt to send to the model.
        system_prompt : str
           The system prompt to send as the initial message to the model.
        temperature : float, optional
            Sampling temperature to use for response generation. Default is 0.7.
        response_format : dict | None, optional
            Response format specification. Example:
            ```
            {
                "type": "json_schema",
                "json_schema": {
                    "name": "response_schema",
                    "schema": json_schema,
                }
            }
            ```
        extra_body : dict | None, optional
            Additional key/value pairs to be included in the request body.
            Example: {'reasoning': {'effort': 'high'}}.

        Returns
        -------
        str | None
            Content of the first message in the model's response, or None if no content is present.
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            response_format=response_format if response_format else None,
            extra_body=extra_body if extra_body else None,
        )
        return response.choices[0].message.content

    def generate_response_json_based(
        self,
        prompt: str,
        json_schema: dict,
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
    ) -> str | None:
        """
        Generates a JSON-formatted response from the LLM based on the provided prompt and schema.

        Parameters
        ----------
        prompt : str
            The user prompt to be sent to the model.
        system_prompt : str
            The system prompt to be sent as the initial message to the model.
        json_schema : dict
            A JSON Schema dict that defines the expected structure of the model's output.
        system_promt : str | None, optional
            Optional system prompt to supplement the user's message.
        reasoning_mode : Literal["none", "minimal", "low", "medium", "high"], optional
            The level of reasoning effort the model should apply when generating the response.
            Defaults to "none".

        Returns
        -------
        str | None
            The JSON response as a string if the model returns a valid response; otherwise, None.
        """
        return self._generate_response(
            prompt=prompt,
            system_prompt=system_prompt,
            response_format={
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
        system_prompt: str,
        reasoning_mode: Literal["none", "minimal", "low", "medium", "high"] = "none",
        temperature: float | None = None,
    ) -> str:
        """
        Generates a text-formatted response from the LLM based on the provided prompt.
        Offer a choice of reasoning effort levels.
        """
        return self._generate_response(
            prompt,
            system_prompt,
            extra_body={"reasoning": {"effort": reasoning_mode}},
            temperature=temperature,
        )


_llm_client = None


def get_llm_client():
    if _llm_client is None:
        _raw_client = OpenAI(
            api_key=AI_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
        _llm_client = LLMClient(_raw_client, MODEL_NAME)
    return _llm_client
