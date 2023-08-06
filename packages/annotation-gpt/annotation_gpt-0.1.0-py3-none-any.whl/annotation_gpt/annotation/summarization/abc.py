import abc
from typing import Text

from annotation_gpt.schema.result import SummarizationResult


class Summarization(object):
    @abc.abstractmethod
    def process(self, document: Text) -> SummarizationResult:
        pass
