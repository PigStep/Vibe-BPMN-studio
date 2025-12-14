from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # FIXME допиши потом setttings


AI_API_KEY = os.environ["OPEN_ROUTER_API_KEY"]

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
    model="tngtech/deepseek-r1t2-chimera:free",
    messages=[{"role": "user", "content": "What is the meaning of life?"}],
    stream=True,
)
full_response = ""
for chunk in completion:
    if chunk.choices[0].delta.content:
        full_response += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end="", flush=True)
# print(completion.choices[0].message.content)
