import random
from nxtools import get_files
from pohadkomat.common import config


def get_clips() -> list[str]:
    """Returns a list of relative paths to downloaded mp3s."""
    return [
        f.path
        for f in get_files(
            config.download_path,
            relative_path=True,
            recursive=True,
            exts=["mp3"],
        )
    ]


def get_batch() -> list[str]:
    """Return a list of urls to play in the batch."""
    result = []
    for i in range(config.clips_per_batch):
        result.append(f"{config.access_url}/media/{random.choice(get_clips())}")
    return result
