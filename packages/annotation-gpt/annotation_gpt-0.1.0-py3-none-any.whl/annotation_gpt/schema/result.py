from typing import Text, TypedDict


class SummarizationResult(TypedDict):
    """The summarization result."""

    document: Text
    summary: Text
