from fastapi.testclient import TestClient

from src.app.api.v1.artist.router import get_artist_service
from src.app.main import app
from src.app.services.database.artist import ArtistService
from src.tests.conftest import TestingSessionLocal

client = TestClient(app)


def override_get_artist_service() -> ArtistService:
    db = TestingSessionLocal()
    return ArtistService(db)


app.dependency_overrides[get_artist_service] = override_get_artist_service


def test_create_artist() -> None:
    json = {"name": "Keith Sweat"}
    response = client.post("/artist/create", json=json)
    assert response.status_code == 201

    created_artist = response.json()
    assert created_artist["name"] == "Keith Sweat"


# TODO: finish writing artist tests
