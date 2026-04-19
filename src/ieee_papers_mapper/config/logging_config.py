import sys
import logging
from pythonjsonlogger.json import JsonFormatter


def setup_logging(level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger("ieee_logger")
    logger.setLevel(level)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(module)s %(funcName)s %(message)s",
        rename_fields={
            "asctime": "timestamp",
            "levelname": "level",
            "funcName": "function",
        },
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
