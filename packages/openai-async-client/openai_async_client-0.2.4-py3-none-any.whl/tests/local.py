import os

from httpx import Timeout

from openai_async_client import AsyncCreate, Message, ChatCompletionRequest

create = AsyncCreate(api_key=os.environ["OPENAI_API_KEY"])
messages = [
    Message(
        role="user",
        content=f"Hello ChatGPT, Give a brief overview of the Pride and Prejudice by Jane Austen.",
    )
]
response = create.completion(
    ChatCompletionRequest(prompt=messages),
    client_timeout=Timeout(1.0, read=10.0),
    retries=3,
)
