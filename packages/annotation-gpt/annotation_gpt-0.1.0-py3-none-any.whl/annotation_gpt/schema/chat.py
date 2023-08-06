from typing import Text, TypedDict


class Message(TypedDict):
    role: Text  # system, user or assistant
    content: Text
