from ._custom_log_record import CustomLogRecord
from ._step import Step

import logging
from typing import Any
from typing import Self
from typing import Callable
from uuid import uuid4



class CustomLogger(logging.Logger):

    def __init__(self, name, *args, step: Step, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.step = step
        self.init_id = str(uuid4())
        self.additional_custom_dimensions = {}
        self.detached = False
        self.final_name = name
        self._init_name = name
        self._init_args = args
        self._init_kwargs = kwargs

    def handle(self, record: logging.LogRecord) -> CustomLogRecord:
        record: CustomLogRecord = record

        self.step.inc()

        record.step_counter = self.step.peek()

        record.init_id = self.init_id
        record.detached = self.detached
        record.final_name = self.final_name

        custom_dimensions = getattr(record, "custom_dimensions", {})
        custom_dimensions = self.additional_custom_dimensions | custom_dimensions
        record.custom_dimensions = custom_dimensions

        super().handle(record)
    

    def detach_with(self, *, custom_dimensions: dict[str, Any], name_fn: Callable[[str], str] = lambda name: f"Detached{name}") -> Self:
        """
        Example:
        ```
        logger = LoggerConfig(id="TestLogger").get_logger()

        logger.info("hello")

        this_work_id_logger = logger.detach_with(custom_dimensions={"work_id": 123})
        this_work_id_logger.info("from the other side ))")

        logger.info("!")
        ```

        Output:
        ```
        flow 1 > [step 1] [name: TestLogger] - hello
        flow 2 from flow 1 > [step 2] [name: DetachedTestLogger] - detached with custom_dimensions={'work_id': 123}
        flow 2 from flow 1 > [step 3] [name: DetachedTestLogger] - from the other side ))
        flow 1 > [step 2] [name: TestLogger] - !
        ```
        """

        new_logger = CustomLogger(self._init_name, *self._init_args, step=self.step.copy(), **self._init_kwargs)

        new_logger.final_name = name_fn(self._init_name)
        new_logger.init_id = self.init_id
        new_logger.additional_custom_dimensions = custom_dimensions
        new_logger.detached = True

        for handler in self.handlers:
            new_logger.addHandler(handler)

        new_logger.info(f"detached with {custom_dimensions=!r}")

        return new_logger
    

