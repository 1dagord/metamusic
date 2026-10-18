import inspect
import logging
from abc import ABCMeta, abstractmethod
from collections.abc import Callable
from functools import wraps
from typing import Any

import httpx
from fastapi import HTTPException
from fastapi import status as http_status
from tenacity import (
  AsyncRetrying,
  RetryCallState,
  retry_if_exception_type,
  stop_after_attempt,
  wait_exponential,
)

from src.app.core.logging import Loggers
from src.app.core.utils import is_dunder_method

logger = logging.getLogger(Loggers.IO)

NUM_RETRIES = 5
MIN_TIMEOUT = 5  # seconds
MAX_TIMEOUT = 60  # seconds
WAIT_MULTIPLIER = 2.0


class _NetworkOperatorMetaclass(ABCMeta):
  def __new__(mcs, name, bases, namespace):
    func_to_decorator = {
      "download": "_retry",
      "search": "_retry",
    }

    for value in namespace.values():
      if inspect.isfunction(value) and not is_dunder_method(value):
        fn = value.__name__

        if fn in func_to_decorator:
          decorator = getattr(
            mcs,
            func_to_decorator[fn],
          )
          namespace[fn] = decorator(namespace[fn])

        # wrap all functions with the exception handler
        namespace[fn] = mcs._handle_network_exceptions(namespace[fn])

    return super().__new__(mcs, name, bases, namespace)

  @staticmethod
  def _handle_network_exceptions(func: Callable[..., Any]):
    """
    Decorator

    Network exception handling
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
      try:
        return await func(*args, **kwargs)

      except httpx.HTTPStatusError as e:
        error_msg = e.response.text
        logger.exception(error_msg)
        raise HTTPException(
          status_code=e.response.status_code,
          detail=error_msg,
        ) from e

      except httpx.RemoteProtocolError as e:
        error_msg = "Connection likely closed prematurely"
        logger.exception(error_msg)
        raise HTTPException(
          status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
          detail=error_msg,
        ) from e

      except httpx.ReadTimeout as e:
        error_msg = "Connection timeout expired"
        logger.exception(error_msg)
        raise HTTPException(
          status_code=http_status.HTTP_504_GATEWAY_TIMEOUT,
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

  @staticmethod
  def _retry(func: Callable[..., Any]):
    """
    Decorator

    Retry logic for :meth:`download`
    """

    def _log_retry_attempts(retry_state: RetryCallState):
      attempt_num = retry_state.attempt_number
      outcome = retry_state.outcome

      logger.debug(f"Download attempt #{attempt_num} failed with outcome {outcome}. Retrying...")

    retry_strategy = AsyncRetrying(
      retry=retry_if_exception_type(
        (
          httpx.RemoteProtocolError,
          httpx.ReadTimeout,
        )
      ),
      stop=stop_after_attempt(NUM_RETRIES),
      wait=wait_exponential(
        WAIT_MULTIPLIER,
        MIN_TIMEOUT,
        MAX_TIMEOUT,
      ),
      reraise=True,
      after=_log_retry_attempts,
    )

    async def wrapper(*args, **kwargs):
      return await retry_strategy(func, *args, **kwargs)

    return wrapper

  @abstractmethod
  async def search(self) -> Any: ...

  @abstractmethod
  async def download(self) -> Any: ...


class NetworkOperator(metaclass=_NetworkOperatorMetaclass):
  """
  Defines an abstract class to be inherited by any class wishing to
  use network features
  """


# TODO: write async tests for this
