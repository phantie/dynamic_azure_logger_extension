from typing import Union, Literal



__all__ = ["LoggingLevel"]

# Defining the type hint for logging levels
LoggingLevel = Union[
    int,
    Literal[
        "CRITICAL",
        "ERROR",
        "WARNING",
        "INFO",
        "DEBUG",
        "NOTSET"
    ]
]
