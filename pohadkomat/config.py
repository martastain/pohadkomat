__all__ = ["config"]

import os
from typing import Annotated

from pydantic import BaseModel, Field


class Config(BaseModel):
    media_dir: Annotated[
        str,
        Field(title="Media directory"),
    ] = "/media"
    cache_dir: Annotated[
        str,
        Field(title="Cache dircetory"),
    ] = "/cache"
    http_port: Annotated[
        int,
        Field(title="HTTP Port", ge=80, lt=65535),
    ] = 9734
    device_name: Annotated[
        str | None,
        Field(title="Chromecast device name"),
    ] = None
    base_url: Annotated[
        str | None,
        Field(title="Base URL"),
    ] = None


def load_config() -> Config:
    prefix = "pohadkomat_"
    env_data = {}
    for key, value in dict(os.environ).items():
        if not key.lower().startswith(prefix):
            continue
        key = key.lower().removeprefix(prefix)
        if key in Config.__fields__:
            env_data[key] = value
    return Config(**env_data)


config = load_config()
