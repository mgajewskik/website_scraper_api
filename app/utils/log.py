import logging
from logging.config import dictConfig


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "api-logger": {"handlers": ["default"], "level": "DEBUG"},
    },
}

dictConfig(LOG_CONFIG)
logger = logging.getLogger("api-logger")


def log_debug(message: str, exc_info: bool = False):

    logger.debug(message, exc_info=exc_info)
