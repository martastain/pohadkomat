import toml

from pydantic import BaseModel, Field
from nxtools import log_traceback, critical_error


class FeedConfig(BaseModel):
    title: str = Field(...)
    url: str = Field(...)
    artist: str | None = Field(None)


class PohadkomatConfig(BaseModel):
    download_path: str = "data/pohadky/"
    database_path: str = "data/pohadky.db"
    feeds: list[FeedConfig] = Field(default_factory=list)
    default_artist: str = Field("Pohadky") 


def load_config():
    try:
        with open("feeds.toml") as f:
            feeds = toml.load(f).get("feeds", [])
    except Exception:
        log_traceback()
        critical_error()

    return PohadkomatConfig(
        feeds=[FeedConfig(**feed) for feed in feeds],
    )


config = load_config()
