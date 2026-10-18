from fastapi.testclient import TestClient

from src.app.api.v1.track.router import get_track_service
from src.app.main import app
from src.app.services.database.track import TrackService
from src.tests.conftest import TestingSessionLocal

client = TestClient(app)


def override_get_track_service() -> TrackService:
  db = TestingSessionLocal()
  return TrackService(db)


app.dependency_overrides[get_track_service] = override_get_track_service


def test_create_track():
  json = {
    "Persistent ID": "47FF256BD86DDA89",
    "Name": "My Song 6",
    "Size": 7514283,
    "Total Time": 237792,
    "Year": 2020,
    "Artist": ["DeAndre"],
    "BPM": 105,
    "Bit Rate": 256,
    "Sample Rate": 44100,
    "Location": "file:///Users/reallytherealest/Music/iTunes/iTunes%20Media/Music/DeAndre/Unknown%20Album/My%20Song%206.m4a",
  }
  # response = client.post("/track/create", json=json)
  # assert response.status_code == 201

  # created_track = response.json()
  # assert created_track["Year"] == 2020


def test_track_create_artist_read_track_delete_artist_read():
  pass


# TODO: finish writing track tests
