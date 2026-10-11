from pathlib import Path

class Config:
    data_dir: Path = Path(__file__).parent.parent.parent / "data"

config = Config()