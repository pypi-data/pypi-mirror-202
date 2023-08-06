"""Example FastAPI server for rwkv.cpp.

To run this example:

```bash
pip install fastapi uvicorn sse-starlette
export MODEL=../models/7B/...
uvicorn server:app --reload
```

Then visit http://localhost:8000/docs to see the interactive API docs.

"""
import os
import time
import uuid
import json
import pathlib
from typing import List, Optional, Literal, Union, Iterator, Dict
from typing_extensions import TypedDict

import sampling
import tokenizers
import rwkv_cpp_model
import rwkv_cpp_shared_library

import server_types

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, BaseSettings, Field, create_model_from_typeddict
from sse_starlette.sse import EventSourceResponse


class Settings(BaseSettings):
    model: str
    tokens_per_generation: int = 100

app = FastAPI(
    title="RWKV API",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
settings = Settings()

tokenizer_path = pathlib.Path(os.path.abspath(__file__)).parent / '20B_tokenizer.json'
tokenizer = tokenizers.Tokenizer.from_file(str(tokenizer_path))
library = rwkv_cpp_shared_library.load_rwkv_shared_library()
model = rwkv_cpp_model.RWKVModel(library, settings.model)
model_path = settings.model

def generate(prompt, temperature, top_p):
    prompt_tokens = tokenizer.encode(prompt).ids

    init_logits, init_state = None, None

    for token in prompt_tokens:
        init_logits, init_state = model.eval(token, init_state, init_state, init_logits)

    while True:
        logits, state = init_logits.clone(), init_state.clone()
        for _ in range(settings.tokens_per_generation):
            token = sampling.sample_logits(logits, temperature, top_p)
            yield token
            logits, state = model.eval(token, state, state, logits)


def create_completion_or_chunks(
    prompt: str,
    suffix: Optional[str] = None,
    max_tokens: int = 16,
    temperature: float = 0.8,
    top_p: float = 0.95,
    logprobs: Optional[int] = None,
    echo: bool = False,
    stop: List[str] = [],
    stream: bool = False,
) -> Union[Iterator[server_types.Completion], Iterator[server_types.CompletionChunk],]:
    completion_id = f"cmpl-{str(uuid.uuid4())}"
    created = int(time.time())
    completion_tokens: List[int] = []
    prompt_tokens: List[int] = tokenizer.encode(prompt).ids # type: ignore

    text = ""
    returned_characters = 0

    if stop != []:
        stop_sequences = [s for s in stop]
    else:
        stop_sequences = []

    finish_reason = None
    for token in generate(
        prompt,
        top_p=top_p,
        temperature=temperature,
    ):
        if token == 0:
            text  = tokenizer.decode(completion_tokens) # type: ignore
            finish_reason = "stop"
            break
        completion_tokens.append(token)

        all_text: str = tokenizer.decode(completion_tokens) # type: ignore
        any_stop = [s for s in stop_sequences if s in all_text]
        if len(any_stop) > 0:
            first_stop = any_stop[0]
            text = all_text[: all_text.index(first_stop)]
            finish_reason = "stop"
            break

        if stream:
            start = returned_characters
            longest = 0
            # We want to avoid yielding any characters from
            # the generated text if they are part of a stop
            # sequence.
            for s in stop_sequences:
                for i in range(len(s), 0, -1):
                    if all_text.endswith(s[:i]):
                        if i > longest:
                            longest = i
                        break
            text = all_text[: len(all_text) - longest]
            returned_characters += len(text[start:])
            yield {
                "id": completion_id,
                "object": "text_completion",
                "created": created,
                "model": model_path,
                "choices": [
                    {
                        "text": text[start:],
                        "index": 0,
                        "logprobs": None,
                        "finish_reason": None,
                    }
                ],
            }
        if len(completion_tokens) >= max_tokens:
            text = tokenizer.decode(completion_tokens)
            finish_reason = "length"
            break

    if finish_reason is None:
        finish_reason = "length"

    if stream:
        yield {
            "id": completion_id,
            "object": "text_completion",
            "created": created,
            "model": model_path,
            "choices": [
                {
                    "text": text[returned_characters:],
                    "index": 0,
                    "logprobs": None,
                    "finish_reason": finish_reason,
                }
            ],
        }
        return

    if echo:
        text = prompt + text

    if suffix is not None:
        text = text + suffix

    if logprobs is not None:
        raise NotImplementedError("logprobs not implemented")

    yield {
        "id": completion_id,
        "object": "text_completion",
        "created": created,
        "model": model_path,
        "choices": [
            {
                "text": text,
                "index": 0,
                "logprobs": None,
                "finish_reason": finish_reason,
            }
        ],
        "usage": {
            "prompt_tokens": len(prompt_tokens),
            "completion_tokens": len(completion_tokens),
            "total_tokens": len(prompt_tokens) + len(completion_tokens),
        },
    }

def completion(
    prompt: str,
    suffix: Optional[str] = None,
    max_tokens: int = 128,
    temperature: float = 0.8,
    top_p: float = 0.95,
    logprobs: Optional[int] = None,
    echo: bool = False,
    stop: List[str] = [],
    stream: bool = False,
) -> Union[server_types.Completion, Iterator[server_types.CompletionChunk]]:
    completion_or_chunks = create_completion_or_chunks(
        prompt=prompt,
        suffix=suffix,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        logprobs=logprobs,
        echo=echo,
        stop=stop,
        stream=stream,
    )
    if stream:
        chunks: Iterator[server_types.CompletionChunk] = completion_or_chunks
        return chunks
    completion: server_types.Completion = next(completion_or_chunks)  # type: ignore
    return completion

def convert_text_completion_to_chat(
    completion: server_types.Completion
) -> server_types.ChatCompletion:
    return {
        "id": "chat" + completion["id"],
        "object": "chat.completion",
        "created": completion["created"],
        "model": completion["model"],
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": completion["choices"][0]["text"],
                },
                "finish_reason": completion["choices"][0]["finish_reason"],
            }
        ],
        "usage": completion["usage"],
    }

def convert_text_completion_chunks_to_chat(
    chunks: Iterator[server_types.CompletionChunk],
) -> Iterator[server_types.ChatCompletionChunk]:
    for i, chunk in enumerate(chunks):
        if i == 0:
            yield {
                "id": "chat" + chunk["id"],
                "model": chunk["model"],
                "created": chunk["created"],
                "object": "chat.completion.chunk",
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                        },
                        "finish_reason": None,
                    }
                ],
            }
        yield {
            "id": "chat" + chunk["id"],
            "model": chunk["model"],
            "created": chunk["created"],
            "object": "chat.completion.chunk",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "content": chunk["choices"][0]["text"],
                    },
                    "finish_reason": chunk["choices"][0]["finish_reason"],
                }
            ],
        }

def chat_completion(
    messages: List[server_types.ChatCompletionMessage],
    temperature: float = 0.8,
    top_p: float = 0.95,
    stream: bool = False,
    stop: List[str] = [],
    max_tokens: int = 128,
) -> Union[server_types.ChatCompletion, Iterator[server_types.ChatCompletionChunk]]:
    instructions = """Complete the following chat conversation between the user and the assistant. System messages should be strictly followed as additional instructions."""
    chat_history = "\n".join(
        f'{message["role"]} {message.get("user", "")}: {message["content"]}'
        for message in messages
    )
    PROMPT = f" \n\n### Instructions:{instructions}\n\n### Inputs:{chat_history}\n\n### Response:\nassistant: "
    PROMPT_STOP = ["###", "\nuser", "\nassistant", "\nsystem"]
    completion_or_chunks = completion(
        prompt=PROMPT,
        stop=PROMPT_STOP + stop,
        temperature=temperature,
        top_p=top_p,
        stream=stream,
        max_tokens=max_tokens,
    )
    if stream:
        chunks: Iterator[CompletionChunk] = completion_or_chunks  # type: ignore
        return convert_text_completion_chunks_to_chat(chunks)
    else:
        completion: Completion = completion_or_chunks  # type: ignore
        return convert_text_completion_to_chat(completion)

class CreateCompletionRequest(BaseModel):
    prompt: str
    suffix: Optional[str] = Field(None)
    max_tokens: int = 16
    temperature: float = 0.8
    top_p: float = 0.95
    echo: bool = False
    stop: List[str] = []
    stream: bool = False

    # ignored or currently unsupported
    model: Optional[str] = Field(None)
    n: Optional[int] = 1
    logprobs: Optional[int] = Field(None)
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    best_of: Optional[int] = 1
    logit_bias: Optional[Dict[str, float]] = Field(None)
    user: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "prompt": "\n\n### Instructions:\nWhat is the capital of France?\n\n### Response:\n",
                "stop": ["\n", "###"],
            }
        }



CreateCompletionResponse = create_model_from_typeddict(server_types.Completion)


@app.post(
    "/v1/completions",
    response_model=CreateCompletionResponse,
)
def create_completion(request: CreateCompletionRequest):
    completion_or_chunks = completion(
        **request.dict(
            exclude={
                "model",
                "n",
                "logprobs",
                "frequency_penalty",
                "presence_penalty",
                "best_of",
                "logit_bias",
                "user",
                "top_k",
                "repeat_penalty"
            }
        )
    )
    if request.stream:
        _chunks: Iterator[server_types.CompletionChunk] = completion_or_chunks  # type: ignore
        return EventSourceResponse(dict(data=json.dumps(chunk)) for chunk in _chunks)
    _completion: server_types.Completion = completion_or_chunks  # type: ignore
    return _completion


class CreateEmbeddingRequest(BaseModel):
    model: Optional[str]
    input: str
    user: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "input": "The food was delicious and the waiter...",
            }
        }


CreateEmbeddingResponse = create_model_from_typeddict(server_types.Embedding)


@app.post(
    "/v1/embeddings",
    response_model=CreateEmbeddingResponse,
)
def create_embedding(request: CreateEmbeddingRequest):
    raise NotImplementedError()


class ChatCompletionRequestMessage(BaseModel):
    role: Union[Literal["system"], Literal["user"], Literal["assistant"]]
    content: str
    user: Optional[str] = None


class CreateChatCompletionRequest(BaseModel):
    model: Optional[str]
    messages: List[ChatCompletionRequestMessage]
    temperature: float = 0.8
    top_p: float = 0.95
    stream: bool = False
    stop: List[str] = []
    max_tokens: int = 128

    # ignored or currently unsupported
    model: Optional[str] = Field(None)
    n: Optional[int] = 1
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    logit_bias: Optional[Dict[str, float]] = Field(None)
    user: Optional[str] = Field(None)

    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    ChatCompletionRequestMessage(
                        role="system", content="You are a helpful assistant."
                    ),
                    ChatCompletionRequestMessage(
                        role="user", content="What is the capital of France?"
                    ),
                ]
            }
        }


CreateChatCompletionResponse = create_model_from_typeddict(server_types.ChatCompletion)


@app.post(
    "/v1/chat/completions",
    response_model=CreateChatCompletionResponse,
)
async def create_chat_completion(
    request: CreateChatCompletionRequest,
) -> Union[server_types.ChatCompletion, EventSourceResponse]:
    completion_or_chunks = chat_completion(
        **request.dict(
            exclude={
                "model",
                "n",
                "presence_penalty",
                "frequency_penalty",
                "logit_bias",
                "user",
            }
        ),
    )

    if request.stream:

        async def server_sent_events(
            chat_chunks: Iterator[server_types.ChatCompletionChunk],
        ):
            for chat_chunk in chat_chunks:
                yield dict(data=json.dumps(chat_chunk))
            yield dict(data="[DONE]")

        _chunks: Iterator[server_types.ChatCompletionChunk] = completion_or_chunks  # type: ignore

        return EventSourceResponse(
            server_sent_events(_chunks),
        )
    _completion: server_types.ChatCompletion = completion_or_chunks  # type: ignore
    return _completion


class ModelData(TypedDict):
    id: str
    object: Literal["model"]
    owned_by: str
    permissions: List[str]


class ModelList(TypedDict):
    object: Literal["list"]
    data: List[ModelData]


GetModelResponse = create_model_from_typeddict(ModelList)


@app.get("/v1/models", response_model=GetModelResponse)
def get_models() -> ModelList:
    return {
        "object": "list",
        "data": [
            {
                "id": settings.model,
                "object": "model",
                "owned_by": "me",
                "permissions": [],
            }
        ],
    }


if __name__ == "__main__":
    import os
    import uvicorn

    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 8000)))
