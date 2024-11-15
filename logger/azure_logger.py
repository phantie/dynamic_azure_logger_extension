"""
Deprecated module to import from

Use 

    from logger import get_logger

Instead of

    from logger.azure_logger import AzureLogger

"""

from ._custom_az_log_handler import CustomAzureLogHandler
from .default_formatters import STDOUT_FORMATTER, AZ_APPINSIGHTS_FORMATTER

import functools
import logging
import os


class AzureLogger:
    """Exists for backward compatibility, use get_logger instead"""

    @staticmethod
    @functools.cache
    def get_logger(
            service_name: str = "service_logger",
            logger_level: str = "DEBUG",
            use_stdout_handler: bool = True,
            appinsights_conn_str: str = os.environ.get('APPLICATIONINSIGHTS_CONNECTION_STRING'),
    ) -> logging.Logger:
        print("! logger.azure_logger.AzureLogger.get_logger is deprecated, use logger.get_logger instead")

        assert isinstance(appinsights_conn_str, str), "APPLICATIONINSIGHTS_CONNECTION_STRING env var must be set"

        logger = logging.getLogger(service_name)
        logger.setLevel(logger_level)

        az_log_handler = CustomAzureLogHandler(connection_string=appinsights_conn_str)
        az_log_handler.setFormatter(AZ_APPINSIGHTS_FORMATTER)
        az_log_handler.setLevel(logger_level)
        logger.addHandler(az_log_handler)

        if use_stdout_handler:
            stdout_handler = logging.StreamHandler()
            stdout_handler.setFormatter(STDOUT_FORMATTER)
            stdout_handler.setLevel(logger_level)
            logger.addHandler(stdout_handler)

        return logger
