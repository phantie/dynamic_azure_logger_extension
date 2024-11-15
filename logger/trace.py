"""
Reimports from opencensus.trace with examples


Example:
```python

from logger.trace import Tracer
from logger.trace import AzureExporter

tracer = Tracer(
    exporter=AzureExporter(connection_string=...),
)

with tracer.span(name="my-span"):
    ... # do stuff

```
"""


from opencensus.trace import config_integration
from opencensus.trace.tracer import Tracer
from opencensus.ext.azure.trace_exporter import AzureExporter


__all__ = [
    "Tracer",
    "AzureExporter"
]


config_integration.trace_integrations(['logging'])


