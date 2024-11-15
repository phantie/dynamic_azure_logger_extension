import os
from logger import get_logger
from logger import stdout_log_handler
from logger import az_appinsights_log_handler


from logger.custom_formatter import CustomFormatter

STDOUT_FORMATTER = CustomFormatter(
    "[step {step}] "
    "[init_id: %(init_id)s] "
    "[detached: %(detached)s] "
    "%(message)s"
)

logger = get_logger(id="test",
    handlers=[
        stdout_log_handler(
            level="DEBUG",
            formatter=STDOUT_FORMATTER, # override default formatter for example
        ),
        # az_appinsights_log_handler(level="DEBUG", con_str=os.environ.get("APPINS"))
    ]
)


logger.info("HELLO")
logger.info("WORLD")
logger.info("!!!")



logger = get_logger(id="test",
    handlers=[
        stdout_log_handler(level="DEBUG"),
        # az_appinsights_log_handler(level="DEBUG", con_str=os.environ.get("APPINS"))
    ]
)

logger.info("hello") # does NOT contain item_id in customDimensions
for item_id in [13, 42]:
    this_processing_item_logger = logger.detach_with(custom_dimensions={"item_id": item_id})
    this_processing_item_logger.info("from the other side") # contains item_id in customDimensions
    this_processing_item_logger.info("))") # contains item_id in customDimensions
