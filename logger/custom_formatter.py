from ._custom_log_record import CustomLogRecord

import logging 



class CustomFormatter(logging.Formatter):
    """
    Formats custom fields in message
    Supported fields: step, init_id

    Example:
    '''
    f = CustomFormatter(
        "[step {step}] "
        "[init_id {init_id}] "
        "[detached {detached}] "
        "[%(asctime)s] "
    )
    handler.setFormatter(f)
    '''
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from copy import copy
        self._permanent_style = copy(self._style)

    def format(self, record: CustomLogRecord):
        # Customize log message format
        self._style._fmt = self._permanent_style._fmt.format(
            step = record.step_counter,
            init_id = record.init_id,
            detached = record.detached,
        )
        return super().format(record)
