from core.config import config
from services.io.parser import PlaylistParser

p = PlaylistParser(config.data_dir / "Library.xml")

print(list(p.tracks.values())[0])
