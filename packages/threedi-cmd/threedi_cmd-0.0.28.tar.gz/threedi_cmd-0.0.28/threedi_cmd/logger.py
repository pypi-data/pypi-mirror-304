import logging
from rich.logging import RichHandler
from functools import lru_cache


USE_RICH_LOGGING = True

@lru_cache()
def get_logger(level: str):
    handlers = []
    if USE_RICH_LOGGING:
        handlers.append(RichHandler(rich_tracebacks=True))

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=handlers,
    )

    if not USE_RICH_LOGGING:
        logger = logging.getLogger("rich")
    else:
        logger = logging.getLogger("threedi_cmd")
    return logger
