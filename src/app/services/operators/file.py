import inspect
import logging
from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any

from fastapi import HTTPException
from fastapi import status as http_status

from src.app.core.logging import Loggers
from src.app.core.utils import is_dunder_method

logger = logging.getLogger(Loggers.DB)


class _FileOperatorMetaclass(ABC, ABCMeta):
    def __new__(mcs, name, bases, namespace):
        # wrap all functions with the wrapper defined below
        for value in namespace.values():
            if inspect.isfunction(value) and not is_dunder_method(value):
                fn = value.__name__
                namespace[fn] = mcs._handle_file_exceptions(namespace[fn])

        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _handle_file_exceptions(func: Callable[..., Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except FileNotFoundError as e:
                error_msg = "File not found"
                logger.exception(error_msg)
                raise HTTPException(
                    status_code=http_status.HTTP_404_NOT_FOUND,
                    detail=error_msg,
                ) from e

            except Exception as e:
                error_msg = "An unexpected error occurred"
                logger.exception(error_msg)
                raise HTTPException(
                    status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error_msg,
                ) from e

        return wrapper

    @abstractmethod
    def parse(self, file: Path) -> None: ...


class FileOperator(ABC, metaclass=_FileOperatorMetaclass):
    """
    Defines an abstract class to be inherited by any class wishing to
    interact with files
    """
