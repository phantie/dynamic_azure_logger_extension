### Init logger

```python
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

```


## Example of adding dynamic fields to logger messages

Logging this:
```python
logger.info("HELLO")
logger.info("WORLD")
logger.info("!!!")
```

Dynamic attributes [step, detached, init_id] are dynamically placed:
```
[step 1] [init_id: 8de6366a-5fdd-4ca4-a888-cc2d4cd8e99b] [detached: False] HELLO
[step 2] [init_id: 8de6366a-5fdd-4ca4-a888-cc2d4cd8e99b] [detached: False] WORLD
[step 3] [init_id: 8de6366a-5fdd-4ca4-a888-cc2d4cd8e99b] [detached: False] !!!
```

## (Azure Application Insights) Example of adding custom_dimensions to every log message

```python

logger.info("hello") # does NOT contain item_id in customDimensions
for item_id in [13, 42]:
    this_processing_item_logger = logger.detach_with(custom_dimensions={"item_id": item_id})
    this_processing_item_logger.info("from the other side") # contains item_id in customDimensions
    this_processing_item_logger.info("))") # contains item_id in customDimensions

```

Output:
```
[step 1] [init_id: 3c912f78-e2dd-4705-ac10-cf5dc5a5caca] [detached: False] hello
[step 2] [init_id: 3c912f78-e2dd-4705-ac10-cf5dc5a5caca] [detached: True] detached with custom_dimensions={'item_id': 42}
[step 3] [init_id: 3c912f78-e2dd-4705-ac10-cf5dc5a5caca] [detached: True] from the other side
[step 4] [init_id: 3c912f78-e2dd-4705-ac10-cf5dc5a5caca] [detached: True] ))
```

Also works as expected for parallel processing, allowing to filter logs in App Insights
by item_id in this case, resulting in sequential step counter for message groups:
```
traces | where customDimensions.item_id == 42
traces | where customDimensions.item_id == 13
```

## (Azure Application Insights) Other log filtering
```
traces | where customDimensions.init_id == "533416e0-1177-40ae-9233-16b8de17dcc1"
traces | where customDimensions.step == 1
traces | where customDimensions.detached == true
```

All supported by default customDimensions.{attribute}:
```
message, step, init_id, detached, final_name, filename, funcName, level, levelno, lineNumber, module, msecs, name, fileName, process, processName, relativeCreated, thread, threadName
```