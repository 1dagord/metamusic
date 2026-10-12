import inspect
import logging
from abc import ABCMeta
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException
from fastapi import status as http_status
from fastapi.exceptions import ResponseValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

from src.core.logging import Loggers

logger = logging.getLogger(Loggers.DB)


class _DatabaseOperatorMetaclass(ABCMeta):
    def __new__(mcs, name, bases, namespace):
        # wrap all functions with the wrapper defined below
        is_dunder_method = lambda fn: fn.startswith("__") and fn.endswith("__")

        for value in namespace.values():
            if inspect.isfunction(value) and not is_dunder_method(
                fn := value.__name__
            ):
                namespace[fn] = mcs._handle_database_exceptions(namespace[fn])

        return super().__new__(mcs, name, bases, namespace)

    @staticmethod
    def _handle_database_exceptions(func: Callable[[], Any]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except OperationalError as e:
                error_msg = (
                    "An error occurred while interacting with the database"
                )
                logger.exception(error_msg)
                raise HTTPException(
                    status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=error_msg,
                ) from e

            except IntegrityError as e:
                error_msg = "Failed to commit to database"
                logger.exception(error_msg)
                raise HTTPException(
                    status_code=http_status.HTTP_409_CONFLICT,
                    detail=error_msg,
                ) from e

            except ResponseValidationError as e:
                error_msg = "Input data validation failed"
                logger.exception(error_msg)
                raise HTTPException(
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    detail=error_msg,
                ) from e

            except HTTPException:
                raise

            except Exception as e:
                error_msg = "An unexpected error occurred"
                logger.exception(error_msg)
                raise HTTPException(
                    status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error_msg,
                ) from e

        return wrapper


class DatabaseOperator(metaclass=_DatabaseOperatorMetaclass):
    """
    Defines an abstract class to be inherited by any class wishing to
    interact directly with the database
    """
