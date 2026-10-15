from fastapi.testclient import TestClient

from src.app.api.v1.genre.router import get_genre_service
from src.app.main import app
from src.app.services.database.genre import GenreService
from src.tests.conftest import TestingSessionLocal

client = TestClient(app)


def override_get_genre_service() -> GenreService:
    db = TestingSessionLocal()
    return GenreService(db)


app.dependency_overrides[get_genre_service] = override_get_genre_service


def test_create_genre() -> None:
    json = {"name": "R&B"}
    response = client.post("/genre/create", json=json)
    assert response.status_code == 201

    created_genre = response.json()
    assert created_genre["name"] == "R&B"


# TODO: finish writing genre tests
