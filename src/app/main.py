from contextlib import asynccontextmanager
from logging import DEBUG, INFO

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.app.api.v1.artist.router import ArtistRouter
from src.app.api.v1.genre.router import GenreRouter
from src.app.api.v1.track.router import TrackRouter
from src.app.core.config import config
from src.app.db.config import engine, initialize_database, teardown_database


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_database(engine)

    try:
        yield

    finally:
        teardown_database(engine)


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
    f"http://{config.host}:{config.port}",
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=config.host,
        port=config.port,
        log_level=(DEBUG if config.debug else INFO),
        log_config=None,
    )
