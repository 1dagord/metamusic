import logging
import plistlib
from pathlib import Path
from typing import Any

from src.app.core.logging import Loggers
from src.app.services.operators.file import FileOperator

logger = logging.getLogger(Loggers.IO)


class FileIOService(FileOperator):
    def __init__(self):
        pass

    def parse(self, file: Path | str | bytes) -> dict[str, Any]:
        if isinstance(file, Path):
            with open(file=file, mode="rb") as fp:
                data = plistlib.load(fp)

        elif isinstance(file, str):
            data = plistlib.loads(file, fmt=plistlib.PlistFormat.FMT_XML)

        else:
            data = plistlib.loads(file)

        return data
