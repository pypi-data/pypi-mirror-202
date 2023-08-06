import logging
from rich.console import Console


console = Console()


class Settings(object):
    logger_name = "annotation-gpt"


settings = Settings()

logger = logging.getLogger(settings.logger_name)
