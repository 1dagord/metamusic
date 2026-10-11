import logging
import plistlib
from pathlib import Path

from core.logging import Loggers

logger = logging.getLogger(Loggers.IO)


class PlaylistParser:
    def __init__(self, file: Path):
        self._data = self.read(file)

    def read(self, file: Path):
        try:
            with open(file=file, mode="rb") as fp:
                data = plistlib.load(fp)

            return data

        except FileNotFoundError:
            logger.exception(f"File {file} not found")
            raise

    @property
    def tracks(self):
        return self._data.get("Tracks")
