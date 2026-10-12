from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.v1.artist.router import ArtistRouter
from src.api.v1.genre.router import GenreRouter
from src.api.v1.track.router import TrackRouter
from src.core.config import config
from src.db.config import engine, initialize_database
from src.services.io.parser import PlaylistParser


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_database(engine)

    try:
        yield
    finally:
        pass


app = FastAPI(
    title=config.app_name,
    debug=config.debug,
    lifespan=lifespan,
)

app.include_router(TrackRouter)
app.include_router(GenreRouter)
app.include_router(ArtistRouter)

origins = [
    "http://localhost",
    f"http://localhost:{config.port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return JSONResponse({"message": "Hello World!"})


p = PlaylistParser(config.data_dir / "Library.xml")

print(list(p.tracks.values())[0])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level=("debug" if config.debug else "info"),
    )
