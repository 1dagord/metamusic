import ast
from pathlib import Path

import requests
from fake_useragent import UserAgent
from requests.models import Response

from src.app.core.config import config


class SongDownloader:
  def __init__(self):
    self.user_agent = UserAgent()
    self.root_url = "https://tracks.monochrome.st"

  def search(self, song_name: str, artist: str) -> Response:
    """
    Searches for a song on Monochrome
    """
    url = self.root_url + "/search"
    headers = {"User-Agent": self.user_agent.random}
    params = {"q": f"{song_name} by {artist}"}
    results = requests.get(url, headers=headers, params=params)

    return results

  def download(self, track_id: str) -> Response:
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
    results = requests.get(url, headers=headers, stream=True)

    return results

  def save(self, response: requests.Response, out_file: Path | str) -> None:
    """
    Saves streamed data to a file
    """
    if response.status_code == 200:
      chunk_size = 8192

      with open(out_file, "wb") as f:
        f.writelines(response.iter_content(chunk_size))

  def _save_from_file(self, in_file: Path | str, out_file: Path | str):
    with open(out_file, mode="wb") as of, open(in_file, mode="r") as f:
      hex_data = f.read()
      content = ast.literal_eval(hex_data)
      of.write(content)


if __name__ == "__main__":
  sd = SongDownloader()

  song_name = "Brown Sugar"
  artist = "D'Angelo"

  result = sd.search(song_name, artist)

  tracks = result.json().get("tracks")
  track_id = tracks[0].get("trackId")

  response = sd.download(track_id)

  out_file = config.data_dir / song_name
  in_file = config.data_dir / "hex_data.txt"

  sd.save(response, str(out_file) + ".flac")

  # sd._save_from_file(in_file, str(out_file) + ".flac")
