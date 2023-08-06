from typing import Any, List, Optional, Text, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from annotation_gpt.schema.chat import Message


class CompletionChoice(TypedDict):
    finish_reason: Text
    index: int
    logprobs: Optional[Any]
    text: Text


class CompletionUsage(TypedDict):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class CompletionResult(TypedDict):
    choices: List[CompletionChoice]
    created: int
    id: Text
    model: Text
    object: Text
    usage: CompletionUsage


class ChatCompletionUsage(TypedDict):
    prompt_tokens: Text
    completion_tokens: Text
    total_tokens: Text


class ChatCompletionChoice(TypedDict):
    message: "Message"
    finish_reason: Text
    index: int


class ChatCompletionResult(TypedDict):
    id: Text
    object: Text
    created: int
    model: Text
    usage: ChatCompletionUsage
    choices: List[ChatCompletionChoice]
