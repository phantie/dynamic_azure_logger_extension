from typing import Callable
from typing import Awaitable
import logging


__all__ = ["exc_trace"]



def exc_trace(e: BaseException) -> str:
    """
    Extracts trace from an exception to str
    Useful in inspect_err before unwrap or expect to log trace,
        since without it you only see Panic's stack trace 

    Example:
    '''python    
    print(exc_trace(ZeroDivisionError()))
    '''
    """
    from traceback import format_exception
    return "".join(format_exception(e))


def _handle_exception(e: Exception, logger: logging.Logger) -> None:
    # for routing exceptions to MS Teams
    custom_dimensions = {
        "tag": "my_ocr_error",
    }

    logger.critical(exc_trace(e), extra={"custom_dimensions": custom_dimensions})
    logger.critical(repr(e))

async def _aio_handle_exception(e: Exception, logger: logging.Logger) -> None:
    _handle_exception(e, logger)

async def aio_ensure_exception_logging(
    fn: Callable[[], Awaitable[None]],
    logger: logging.Logger,
    handle_exception: Callable[[Exception, logging.Logger], Awaitable[None]] = _aio_handle_exception,
) -> None:
    """
    logs caught exceptions of an coroutine wrapped in nullary function
    """

    try:
        await fn()
    except Exception as e:
        await handle_exception(e, logger)
        raise e

def ensure_exception_logging(
    fn: Callable[[], None],
    logger: logging.Logger,
    handle_exception: Callable[[Exception, logging.Logger], None] = _handle_exception,
) -> None:
    """
    logs caught exceptions of a nullary function
    """

    try:
        fn()
    except Exception as e:
        handle_exception(e, logger)
        raise e
