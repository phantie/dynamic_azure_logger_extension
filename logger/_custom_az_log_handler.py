from ._custom_log_record import CustomLogRecord

from typing import Any

from opencensus.ext.azure.log_exporter import AzureLogHandler



__all__ = ["CustomAzureLogHandler"]


class CustomAzureLogHandler(AzureLogHandler):
    def emit(self, record: CustomLogRecord):

        def custom_dimensions_from_record(record: CustomLogRecord, properties: set[str]) -> dict[str, Any]:
            """Creates custom_dimensions dict extension from LogRecord"""
            custom_dimensions = {}
            for prop in properties:
               custom_dimensions[prop] = getattr(record, prop)
            custom_dimensions["message"] = record.getMessage()
            custom_dimensions["step"] = record.step_counter
            custom_dimensions["init_id"] = record.init_id
            custom_dimensions["detached"] = record.detached
            custom_dimensions["final_name"] = record.final_name
            return custom_dimensions

        record.custom_dimensions = getattr(record, "custom_dimensions", {}) | custom_dimensions_from_record(
            record,
            # https://docs.python.org/3/library/logging.html
            {
                "filename",
                "funcName",
                # "levelname", # already present as "level"
                "levelno",
                # "lineno", # already present as "lineNumber"
                "module",
                "msecs",
                "name",
                # "pathname", # already present as "fileName"
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
            }
        )

        # print("Emitting with custom_dimensions", record.custom_dimensions)

        super().emit(record)
