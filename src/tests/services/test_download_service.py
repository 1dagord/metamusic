import pytest

from src.app.core.config import config
from src.app.services.io.network.download import SongDownloader


@pytest.mark.skip(reason="Makes a network call. Better to test manually.")
async def _test_song_downloader():
  sd = SongDownloader()

  song_name = "Brown Sugar"
  artist = "D'Angelo"
  album = "Brown Sugar"

  result = await sd.search(song_name, artist, album)

  tracks = result.json().get("tracks")
  track_id = tracks[0].get("trackId")

  response = await sd.download(track_id)

  out_file = config.data_dir / song_name
  in_file = config.data_dir / "hex_data.txt"

  await sd.save(response, str(out_file) + ".flac")

  # sd._save_from_file(in_file, str(out_file) + ".flac")
