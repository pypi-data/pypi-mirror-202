import uuid
from dotenv import load_dotenv
import pandas as pd

from openai_async_client import (
    AsyncCreate,
    Message,
    ChatCompletionRequest,
    SystemMessage,
    OpenAIParams,
)
from openai_async_client.model import EndpointConfig

pd.set_option("display.max_rows", 12)
pd.set_option("display.max_columns", 12)
pd.set_option("display.width", 1000)

load_dotenv()

# Example DataFrame
TEST_INPUTS = [
    "the open society and its enemies by Karl Popper",
    "Das Capital by Karl Marx",
    "Pride and Prejudice by Jane Austen",
    "Frankenstein by Mary Shelley",
    "Moby Dick by  Herman Melville",
]

records = [
    {"author_id": i, "book_id": str(uuid.uuid4())[:6], "book_name": s}
    for i, s in enumerate(TEST_INPUTS)
]
input_df = pd.DataFrame.from_records(records)

create = AsyncCreate()


# Define a mapping function from row to prompt
def chat_prompt_fn(r: pd.Series) -> ChatCompletionRequest:
    message = Message(
        role="user",
        content=f"Hello ChatGPT, Give a brief overview of the book {r.book_name}.",
    )
    # (key Dict is mandatory since results are NOT returned in order)
    key = {"author_id": r.author_id, "book_id": r.book_id}
    return ChatCompletionRequest(
        key=key,
        prompt=[message],
        system=SystemMessage(content="Assistant is providing book reviews"),
        params=OpenAIParams(model="gpt-3.5-turbo"),
    )


# parallel process the DataFrame making up to max_connections concurrent requests to OpenAI endpoint
result_df = create.completions(
    df=input_df,
    request_fn=chat_prompt_fn,
    config=EndpointConfig.CHAT,
    max_connections=4,
)
# print(result_df.columns)
print(result_df.head())
# (result_df columns are the input_df columns plus:
#  "openai_completion" - the completion/s (str/list),
#  "openai_id",
#  "openai_created",
#  "openai_prompt_tokens",
#  "openai_completion_tokens",
#  "openai_total_tokens",
#  "api_error" - http, openai, api error or pd.NA when everything is Okay.
