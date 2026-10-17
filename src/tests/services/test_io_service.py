from fastapi.testclient import TestClient

from src.app.core.config import config
from src.app.main import app
from src.app.services.io.parser import IOService

client = TestClient(app)


def test_parse_service():
    io_service = IOService()
    file = config.data_dir / "Library.xml"

    data = io_service.parse(file)

    assert (
        data["Tracks"]["10107"]["Artist"]
        == "Mach-Hommy, KAYTRANADA & 03 Greedo"
    )

    # print(f"{[entry.get("Artist") for entry in data.get("Tracks").values()] = }")
    # print(
    #     [
    #         entry
    #         for entry in data["Tracks"].values()
    #         if "Mach Hommy" in entry["Artist"]
    #     ],
    #     end="\n\n",
    # )
