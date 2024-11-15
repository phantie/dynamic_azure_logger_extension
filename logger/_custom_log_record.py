import logging
from dataclasses import dataclass
from typing import Optional



@dataclass
class CustomLogRecord(logging.LogRecord):
    """Type hinting for added fields on CustomLogger"""

    step_counter: int
    init_id: str
    custom_dimensions: Optional[dict]
    detached: bool
    final_name: str

