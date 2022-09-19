import toml

from typing import Optional
from pydantic import BaseModel, Field
from nxtools import log_traceback, critical_error


class FeedConfig(BaseModel):
    title: str = Field(...)
    url: str = Field(...)
    artist: Optional[str] = Field(None)


class PohadkomatConfig(BaseModel):
    download_path: str = "data/pohadky/"
    asrun_path: str = "asrun.lst"
    feeds: list[FeedConfig] = Field(default_factory=list)
    default_artist: str = Field("Pohadky")
    clips_per_batch: int = Field(2)
    chromecast_name: str = Field("Living room display")
    http_port: int = Field(9733)
    access_url: str = "http://localhost:9733"


def load_config() -> PohadkomatConfig:
    try:
        with open("pohadkomat.toml") as f:
            settings = toml.load(f).get("pohadkomat", [])
    except Exception:
        log_traceback()
        critical_error()

    try:
        with open("feeds.toml") as f:
            feeds = toml.load(f).get("feeds", [])
    except Exception:
        log_traceback()
        critical_error()

    return PohadkomatConfig(
        feeds=[FeedConfig(**feed) for feed in feeds],
        **settings,
    )


config = load_config()
