from openai import Client
from .config import settings
import logging

client = Client(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


def gpt_completion_steam(prompt, model="gpt-4", temperature=0):
    message = [{"role": "user", "content": prompt}]
    stream = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=temperature,
        stream=True,
    )
    return stream


def completion(prompt, model="gpt-4"):
    result = ""
    stream = gpt_completion_steam(prompt, model)
    logging.info("Start getting completion from OpenAI")
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
        result += chunk.choices[0].delta.content or ""
    logging.info("End getting completion from OpenAI")
    return result
