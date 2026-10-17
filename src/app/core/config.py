from pathlib import Path


class Config:
    app_name: str = "MetaMusic"
    db_name: str = "MM"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000

    @property
    def data_dir(self) -> Path:
        return Path(__file__).parent.parent.parent.parent / "data"

    @property
    def sqlite_db_url(self) -> str:
        return f"sqlite:///./{self.db_name}.db"


config = Config()
