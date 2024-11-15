from ._custom_az_log_handler import CustomAzureLogHandler
from .default_formatters import STDOUT_FORMATTER, AZ_APPINSIGHTS_FORMATTER
from ._level import LoggingLevel
from ._step import Step
from ._custom_logger import CustomLogger

import logging
from typing import Iterable



__all__ = [
    "get_logger",
    "stdout_log_handler",
    "az_appinsights_log_handler",
]


def get_logger(
    *,
    id: str,
    handlers: Iterable[logging.Handler]
) -> CustomLogger:
    """
    Example:
    ```python
    from logger import get_logger
    from logger import stdout_log_handler
    from logger import az_appinsights_log_handler

    logger = get_logger(
        id = "name_for_logger",
        handlers=[
            stdout_log_handler(level="DEBUG"),
            az_appinsights_log_handler(con_str=az_appinsights_con_str, level="DEBUG")
        ]
    )
    ```
    """

    step = Step()

    logger = CustomLogger(id, step=step)
    logger.setLevel("DEBUG")

    for h in handlers:
        logger.addHandler(h)

    return logger


def stdout_log_handler(*, level: LoggingLevel, formatter = STDOUT_FORMATTER):
    h = logging.StreamHandler()
    h.setFormatter(formatter)
    h.setLevel(level)
    return h


def az_appinsights_log_handler(*, con_str: str, level: LoggingLevel, formatter = AZ_APPINSIGHTS_FORMATTER):
    assert isinstance(con_str, str)
    h = CustomAzureLogHandler(connection_string=con_str)
    h.setFormatter(formatter)
    h.setLevel(level)
    return h
