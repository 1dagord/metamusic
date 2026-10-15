import logging.config
from enum import StrEnum, auto


class Loggers(StrEnum):
    IO = auto()
    DB = auto()
    TEST_DB = auto()


logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s: %(message)s"},
        "detailed": {
            "format": "[%(levelname)s] %(asctime)s | %(module)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M%S%z",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "root": {"level": "INFO", "handlers": ["stdout"]},
        Loggers.IO: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stdout"],
        },
        Loggers.DB: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stdout"],
        },
        Loggers.TEST_DB: {
            "level": "DEBUG",
            "propagate": False,
            "handlers": ["stdout"],
        },
    },
}

logging.config.dictConfig(config=logging_config)
