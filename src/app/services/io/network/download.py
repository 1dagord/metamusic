import ast
from pathlib import Path

import aiofiles
import aiofiles.os
import httpx
from fake_useragent import UserAgent
from httpx import Response
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

from src.app.api.v1.track.schema import TrackRead
from src.app.core.config import config
from src.app.services.io.network.dispatch import AsyncDispatcher
from src.app.services.operators.network import NetworkOperator

DEFAULT_TIMEOUT = 5.0  # seconds


class SongDownloader(NetworkOperator):
  CHUNK_SIZE = 8192

  def __init__(self, timeout_seconds: float | None = DEFAULT_TIMEOUT):
    self.user_agent = UserAgent()
    self.client = httpx.AsyncClient(timeout=timeout_seconds)
    self.root_url = "https://tracks.monochrome.st"

  async def search(self, song_name: str, artist: str, album: str) -> Response:
    """
    Searches for a song on Monochrome
    """
    url = self.root_url + "/search"
    headers = {"User-Agent": self.user_agent.random}
    params = {"q": f"{song_name} by {artist} {album}"}
    results = await self.client.get(url, headers=headers, params=params)

    return results

  async def download(self, track_id: str) -> StreamingResponse:
    """
    Downloads song from Monochrome

    :return: reponse with open connection for data streaming
    """
    url = f"{self.root_url}/track/{track_id}"
    headers = {
      "User-Agent": self.user_agent.random,
      "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
      "Sec-Fetch-Dest": "audio",
    }

    request = self.client.build_request(method="GET", url=url, headers=headers)
    response = await self.client.send(request, stream=True)
    response.raise_for_status()

    return StreamingResponse(
      response.aiter_bytes(self.CHUNK_SIZE),
      background=BackgroundTask(response.aclose),
    )

  async def save(self, response: StreamingResponse, out_file: Path | str) -> None:
    """
    Saves streamed data to a file
    """
    # create parent directories if not already present
    await aiofiles.os.makedirs(Path(out_file).parent, exist_ok=True)

    async with aiofiles.open(out_file, "wb") as f:
      async for chunk in response.body_iterator:
        await f.write(chunk)

  def _save_from_file(self, in_file: Path | str, out_file: Path | str):
    with open(out_file, mode="wb") as of, open(in_file, mode="r") as f:
      hex_data = f.read()
      content = ast.literal_eval(hex_data)
      of.write(content)


class AsyncSongDownloader(NetworkOperator):
  """
  Made to perform multiple downloads concurrently
  """

  def __init__(self, timeout_seconds: float | None = DEFAULT_TIMEOUT):
    self.downloader = SongDownloader(timeout_seconds=timeout_seconds)
    self.dispatcher = AsyncDispatcher(self.downloader.client)

  async def _search_download_save(self, track: TrackRead) -> None:
    """
    Performs three dependent async tasks in sequence
    """
    song_name = track.name
    artist = ", ".join(track.artists)
    album = track.album or ""

    search_response = await self.downloader.search(song_name, artist, album)

    tracks = search_response.json().get("tracks")
    track_id = tracks[0].get("trackId")

    download_response = await self.downloader.download(track_id)

    out_file = (
      config.download_dir / artist / album / song_name
      if album
      else config.download_dir / artist / song_name
    )
    await self.downloader.save(download_response, str(out_file) + ".flac")

  async def queue_download(self, track: TrackRead) -> None:
    await self.dispatcher.append_task(
      self._search_download_save,
      track=track,
    )

  async def execute_download(self) -> None:
    await self.dispatcher.run()
