import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from httpx import AsyncClient

NUM_CONCURRENT_TASKS = 10


class AsyncDispatcher:
  """
  Used in conjunction with :class:`SongDownloader` to download songs concurrently
  """

  def __init__(self, client: AsyncClient, num_tasks: int = NUM_CONCURRENT_TASKS):
    self.client = client
    self.semaphore = asyncio.Semaphore(num_tasks)
    self.task_queue = []

  async def _perform_task(self, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> None:
    async with self.semaphore:
      await func(*args, **kwargs)

  async def append_task(self, func: Callable[..., Awaitable[Any]], *args, **kwargs) -> None:
    task = self._perform_task(func, *args, **kwargs)
    self.task_queue.append(task)

  async def run(self) -> None:
    await asyncio.gather(*self.task_queue)
