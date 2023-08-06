from typing import TYPE_CHECKING, List, Text

if TYPE_CHECKING:
    from annotation_gpt.schema.chat import Message


class AnnotationMixin(object):
    def prompt_from_messages(self, messages: List["Message"]) -> Text:
        message_prompts: List[Text] = []
        for message in messages:
            _mp = f"<|im_start|>{message['role']}\n{message['content']}\n<|im_end|>"
            message_prompts.append(_mp)

        prompt = "\n".join(message_prompts) + "\n<|im_start|>assistant\n"
        return prompt

    def format_messages_content(
        self, messages: List["Message"], **kwargs
    ) -> List["Message"]:
        for message in messages:
            message["content"] = message["content"].format(**kwargs)
        return messages
