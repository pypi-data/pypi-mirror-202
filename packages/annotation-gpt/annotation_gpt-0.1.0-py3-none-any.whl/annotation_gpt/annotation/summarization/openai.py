from typing import Dict, Optional, Text, TYPE_CHECKING

from annotation_gpt.annotation.object import AnnotationMixin
from annotation_gpt.config import console, logger
from annotation_gpt.schema.chat import Message
from annotation_gpt.schema.result import SummarizationResult

try:
    import openai
except ImportError:
    console.print(
        "[yellow]Openai is not installed. Please install it by `pip install openai`.[/yellow]"
    )
    logger.warning(
        "Openai is not installed. Please install it by `pip install openai`."
    )

if TYPE_CHECKING:
    from openai.openai_object import OpenAIObject
    from annotation_gpt.schema.openai.result import (
        ChatCompletionResult,
        CompletionResult,
    )


class OpenaiSummarization(AnnotationMixin):
    model = "gpt-3.5-turbo"
    system_prompt = """\
You will summarize document pasted by user.

Instructions:
- Your summary texts should be in language {language_hint}."""
    default_language_hint = "the same as that of the document"
    default_model = "gpt-3.5-turbo"

    def __init__(
        self,
        *args,
        language_hint: Optional[Text] = None,
        model: Optional[Text] = None,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self.language_hint = language_hint or self.default_language_hint
        self.model = model or self.default_model

    def process(
        self,
        document: Text,
        language_hint: Optional[Text] = None,
        use_chatml: bool = False,
        completion_params: Optional[Dict] = None,
    ) -> SummarizationResult:
        document = document.strip()
        language_hint = language_hint or self.language_hint
        completion_params = completion_params or {}

        messages = [
            Message(role="system", content=self.system_prompt),
            Message(role="user", content=document),
        ]
        messages = self.format_messages_content(messages, language_hint=language_hint)

        if use_chatml is True:
            completion_result: "OpenAIObject" = openai.Completion.create(
                model=self.model,
                prompt=self.prompt_from_messages(messages),
                **completion_params,
            )
            completion_result_dict: CompletionResult = (
                completion_result.to_dict_recursive()
            )
            summary = completion_result_dict["choices"][-1]["text"].strip()

        else:
            chat_completion_result: "OpenAIObject" = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                **completion_params,
            )
            chat_completion_result_dict: ChatCompletionResult = (
                chat_completion_result.to_dict_recursive()
            )
            summary = chat_completion_result_dict["choices"][-1]["message"][
                "content"
            ].strip()

        return SummarizationResult(document=document, summary=summary)
