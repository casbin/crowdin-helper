import time
from openai import Client, Stream
from openai.types.chat import ChatCompletionChunk
from crowdin_helper.config import settings
import logging

client = Client(
    api_key=settings.OPENAI_API_KEY,
    base_url=settings.OPENAI_BASE_URL,
)


def gpt_completion_steam(prompt: str, model: str) -> str:
    message = [{"role": "user", "content": prompt}]
    stream: Stream[ChatCompletionChunk] = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=0,
        stream=True,
    )
    logging.info("Start getting completion from OpenAI")
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        result += content
        print(content, end="")
    logging.info("End getting completion from OpenAI")
    return stream


def completion(prompt, model="gpt-4", max_retries=5, delay=3):
    result = None
    num_retries = 0
    while True:
        try:
            result = gpt_completion_steam(prompt, model)
            break
        except Exception as e:
            logging.exception(e)
            num_retries += 1
            if num_retries >= max_retries:
                raise e
            logging.info(f"retrying... {num_retries}/{max_retries}")
            time.sleep(delay)

    return result
