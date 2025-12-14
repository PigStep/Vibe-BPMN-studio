from openai import OpenAI
import os
from dotenv import load_dotenv
from settings import get_settings

settings = get_settings()


AI_API_KEY = settings.OPENROUTER_API_KEY
MODEL_NAME = settings.OPENROUTER_MODEL_NAME

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=AI_API_KEY,
)

completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model=MODEL_NAME,
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
    stream=True,
)
full_response = ""
for chunk in completion:
    if chunk.choices[0].delta.content:
        full_response += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end="", flush=True)
# print(completion.choices[0].message.content)
