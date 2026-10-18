import logging.config
from dataclasses import dataclass
from enum import StrEnum
from logging import DEBUG, INFO

from src.app.core.config import config


class Loggers(StrEnum):
  IO = "io"
  DB = "db"
  TEST_DB = "db.test"


@dataclass
class LoggerManager:
  """
  Centralized settings for all custom loggers
  """

  propagate: bool = False

  @property
  def handlers(self) -> list[str]:
    return ["stdout", "file"]

  @property
  def log_level(self) -> int:
    return DEBUG if config.debug else INFO


logger_manager = LoggerManager()

logging_config = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "simple": {"format": "%(levelname)s: %(message)s"},
    "detailed": {
      "format": "[%(levelname)s] %(asctime)s | %(filename)s > %(module)s: %(message)s",
      "datefmt": "%Y-%m-%dT%H:%M%S%z",
    },
  },
  "handlers": {
    "stdout": {
      "class": "logging.StreamHandler",
      "formatter": "detailed",
      "stream": "ext://sys.stdout",
    },
    "file": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": INFO,
      "formatter": "detailed",
      "filename": f"logs/{config.app_name}.log",
      "maxBytes": 1_000_000,
      "backupCount": 5,
    },
  },
  "loggers": {
    "root": {"level": "INFO", "handlers": logger_manager.handlers},
    Loggers.IO: {
      "level": logger_manager.log_level,
    },
    Loggers.DB: {
      "level": logger_manager.log_level,
    },
    Loggers.TEST_DB: {
      "level": logger_manager.log_level,
    },
  },
}

logging.config.dictConfig(config=logging_config)
