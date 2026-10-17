from fastapi.testclient import TestClient

from src.app.core.config import config
from src.app.main import app
from src.app.services.io.parser import FileIOService

client = TestClient(app)


def test_parse():
    file_io_service = FileIOService()
    file = config.data_dir / "Library.xml"

    data = file_io_service.parse(file)

    assert (
        data["Tracks"]["10107"]["Artist"]
        == "Mach-Hommy, KAYTRANADA & 03 Greedo"
    )
